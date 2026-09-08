from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth_deps import get_current_manager_user
from app.services import image_verifier, rule_engine, decision_engine
import os
import csv
import uuid
import datetime

router = APIRouter()

DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "dataset")
METADATA_PATH = os.path.join(DATASET_DIR, "metadata.csv")
IMAGES_DIR = os.path.join(DATASET_DIR, "images")

def simulate_verification(filename: str, category: str, part: models.Part):
    file_path = os.path.join(IMAGES_DIR, category, filename)
    if not os.path.exists(file_path):
        return "ERROR"
        
    part_requirements = {
        "required_box": part.required_box,
        "required_padding_mm": part.required_padding_mm,
        "required_orientation": part.required_orientation,
        "protective_cover_required": part.protective_cover_required,
        "min_image_quality": 0.80
    }
    
    try:
        with open(file_path, "rb") as f:
            image_data = f.read()
        features = image_verifier.verify_image(
            image_data, 
            metadata={"filename": filename, **part_requirements}
        )
        rule_results = rule_engine.evaluate_rules(part_requirements, features)
        decision = decision_engine.make_decision(
            rule_results, 
            visual_confidence=features.get("confidence", 0.90), 
            image_quality=features.get("image_quality", 0.90)
        )
        return decision["decision"]
    except Exception as e:
        return "ERROR"


@router.get("/test-harness")
def run_test_harness(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_manager_user)):
    if not os.path.exists(METADATA_PATH):
        return {"error": "Metadata not found"}

    part = db.query(models.Part).filter(models.Part.id == 1).first()
    if not part:
        return {"error": "Part not found"}

    test_cases = []
    with open(METADATA_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_cases.append(row)
            if len(test_cases) >= 15:
                break

    results = []
    for case in test_cases:
        expected = case["expected_decision"].upper()
        # Convert expected from DO NOT DISPATCH / HUMAN REVIEW to standard PASS/FAIL/MANUAL_REVIEW for internal tests
        if expected == "DO NOT DISPATCH":
            expected_decision = "FAIL"
        elif expected == "HUMAN REVIEW":
            expected_decision = "MANUAL_REVIEW"
        else:
            expected_decision = "PASS"

        actual = simulate_verification(case["filename"], case["category"], part).upper()
        status = "PASS" if actual == expected_decision else "FAIL"
        
        results.append({
            "id": case["filename"],
            "description": f"Test case for {case['category']}",
            "expected": expected_decision,
            "actual": actual,
            "status": status
        })

    return results

@router.get("/run")
@router.post("/run")
def run_experiment(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_manager_user)):
    if not os.path.exists(METADATA_PATH):
        return {"error": "Metadata not found"}

    part = db.query(models.Part).filter(models.Part.id == 1).first()
    
    test_cases = []
    with open(METADATA_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_cases.append(row)

    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0
    manual_reviews = 0

    for case in test_cases:
        expected = case["expected_decision"].upper()
        actual = simulate_verification(case["filename"], case["category"], part).upper()
        
        if expected == "DO NOT DISPATCH":
            expected = "FAIL"
        elif expected == "HUMAN REVIEW":
            expected = "MANUAL_REVIEW"
        else:
            expected = "PASS"

        if actual == "MANUAL_REVIEW":
            manual_reviews += 1
            
        # Treat MANUAL_REVIEW as FAIL for strict binary metric calculation
        binary_actual = "FAIL" if actual in ["FAIL", "MANUAL_REVIEW"] else "PASS"
        binary_expected = "FAIL" if expected in ["FAIL", "MANUAL_REVIEW"] else "PASS"

        if binary_expected == "FAIL":
            if binary_actual == "FAIL":
                true_positive += 1
            else:
                false_negative += 1
        elif binary_expected == "PASS":
            if binary_actual == "PASS":
                true_negative += 1
            else:
                false_positive += 1

    total = true_positive + true_negative + false_positive + false_negative
    accuracy = (true_positive + true_negative) / total if total > 0 else 0
    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    total_actual_failed = true_positive + false_negative
    total_failed_detected_before_dispatch = true_positive
    pddr = total_failed_detected_before_dispatch / total_actual_failed if total_actual_failed > 0 else 0
    
    return {
        "run_id": str(uuid.uuid4()),
        "name": f"Validation Run {datetime.datetime.now().strftime('%Y-%m-%d')}",
        "dataset_size": total,
        "metrics": {
            "TP": true_positive,
            "TN": true_negative,
            "FP": false_positive,
            "FN": false_negative,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "pddr": pddr,
            "manual_review_rate": manual_reviews / total if total > 0 else 0
        }
    }

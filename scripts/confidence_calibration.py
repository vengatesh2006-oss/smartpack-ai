import os
import csv
import json

from backend.app.services.image_verifier import verify_image
from backend.app.services.rule_engine import evaluate_rules
from backend.app.services.decision_engine import make_decision

DATASET_DIR = "dataset"
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
METADATA_FILE = os.path.join(DATASET_DIR, "metadata.csv")
RESULTS_DIR = "results"

def load_metadata():
    records = []
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            reader = csv.DictReader(f)
            records = list(reader)
    return {r['filename']: r for r in records}

def run_calibration():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    metadata = load_metadata()
    
    # Brackets: [0.0-0.7), [0.7-0.85), [0.85-1.0]
    buckets = {
        "Low Confidence (0.00-0.69)": {"count": 0, "correct": 0, "total_conf": 0.0},
        "Medium Confidence (0.70-0.84)": {"count": 0, "correct": 0, "total_conf": 0.0},
        "High Confidence (0.85-1.00)": {"count": 0, "correct": 0, "total_conf": 0.0}
    }

    results = []

    for category in os.listdir(IMAGES_DIR):
        cat_path = os.path.join(IMAGES_DIR, category)
        if not os.path.isdir(cat_path): continue

        for filename in os.listdir(cat_path):
            if not (filename.endswith('.jpg') or filename.endswith('.png')): continue
            
            meta = metadata.get(filename, {})
            # Mock requirement extraction based on part
            part_requirements = {
                "required_box": "Standard",
                "required_padding_mm": 10.0,
                "required_orientation": "Upright",
                "protective_cover_required": True,
                "filename": filename
            }

            img_path = os.path.join(IMAGES_DIR, category, filename)
            try:
                with open(img_path, "rb") as f:
                    img_bytes = f.read()
            except:
                continue

            features = verify_image(img_bytes, metadata=part_requirements)
            rule_results = evaluate_rules(part_requirements, features)
            decision = make_decision(
                rule_results, 
                visual_confidence=features.get("confidence", 0.90),
                image_quality=features.get("image_quality", 0.90)
            )

            # Ground truth: correct packing should PASS, anything else should FAIL or MANUAL_REVIEW
            expected = "PASS" if category == "correct" else "FAIL"
            if expected == "FAIL" and decision["decision"] in ["FAIL", "MANUAL_REVIEW"]:
                is_correct = True
            elif expected == "PASS" and decision["decision"] == "PASS":
                is_correct = True
            else:
                is_correct = False

            conf = features.get("confidence", 0.90)
            
            if conf < 0.70:
                bucket = "Low Confidence (0.00-0.69)"
            elif conf < 0.85:
                bucket = "Medium Confidence (0.70-0.84)"
            else:
                bucket = "High Confidence (0.85-1.00)"

            buckets[bucket]["count"] += 1
            buckets[bucket]["total_conf"] += conf
            if is_correct:
                buckets[bucket]["correct"] += 1

            results.append({
                "filename": filename,
                "category": category,
                "predicted": decision["decision"],
                "expected": expected,
                "confidence": conf,
                "correct": is_correct,
                "reason": decision["explanation"]
            })

    # Calculate ECE
    ece = 0.0
    total_samples = len(results)
    
    for b_name, b_stats in buckets.items():
        if b_stats["count"] > 0:
            acc = b_stats["correct"] / b_stats["count"]
            avg_conf = b_stats["total_conf"] / b_stats["count"]
            b_stats["accuracy"] = acc
            b_stats["avg_confidence"] = avg_conf
            
            # ECE component: (|acc - avg_conf| * count / total)
            ece += abs(acc - avg_conf) * (b_stats["count"] / total_samples)

    output_data = {
        "total_samples": total_samples,
        "ece": ece,
        "buckets": buckets,
        "results": results
    }

    with open(os.path.join(RESULTS_DIR, "confidence_calibration.json"), "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Calibration finished. ECE: {ece:.4f}")

if __name__ == "__main__":
    run_calibration()

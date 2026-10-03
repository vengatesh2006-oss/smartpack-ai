import os
import csv
import json
from collections import defaultdict

from backend.app.services.image_verifier import verify_image
from backend.app.services.rule_engine import evaluate_rules
from backend.app.services.decision_engine import make_decision

DATASET_DIR = "dataset"
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
METADATA_FILE = os.path.join(DATASET_DIR, "metadata.csv")
PREDICTIONS_FILE = "results/dataset_predictions.csv"
JSON_STATS = "results/dataset_stats.json"

def run_audit():
    if not os.path.exists("results"):
        os.makedirs("results")

    # Load metadata
    expected_labels = {}
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            for r in csv.DictReader(f):
                expected_labels[r['filename']] = r['category']

    predictions = []
    class_stats = defaultdict(lambda: {'total': 0, 'pred_outcomes': defaultdict(int), 'automatic': 0, 'manual': 0, 'correct': 0, 'incorrect': 0})
    
    total_images = 0
    tp = 0; tn = 0; fp = 0; fn = 0; manual_reviews = 0

    buckets = {
        "Low (0.00-0.69)": {"count": 0, "correct": 0, "manual": 0, "total_conf": 0.0},
        "Medium (0.70-0.84)": {"count": 0, "correct": 0, "manual": 0, "total_conf": 0.0},
        "High (0.85-1.00)": {"count": 0, "correct": 0, "manual": 0, "total_conf": 0.0}
    }

    # Iterate actual files to prevent assumptions
    for category in os.listdir(IMAGES_DIR):
        cat_path = os.path.join(IMAGES_DIR, category)
        if not os.path.isdir(cat_path): continue

        for filename in os.listdir(cat_path):
            if not filename.endswith('.jpg'): continue
            total_images += 1
            img_path = os.path.join(cat_path, filename)
            
            with open(img_path, "rb") as f:
                img_bytes = f.read()

            reqs = {
                "required_box": "Standard",
                "required_padding_mm": 10.0,
                "required_orientation": "Upright",
                "protective_cover_required": True
            }

            features = verify_image(img_bytes, metadata=reqs)
            rules = evaluate_rules(reqs, features)
            decision = make_decision(rules, features["confidence"], features["image_quality"])

            pred_state = decision["decision"]
            reason = decision["explanation"]
            conf = features["confidence"]
            
            gt_state = "PASS" if category == "correct" else "FAIL"
            is_manual = pred_state == "MANUAL_REVIEW"
            
            if is_manual:
                is_correct = (gt_state == "FAIL")
            else:
                is_correct = (pred_state == gt_state)

            if is_manual:
                manual_reviews += 1
            else:
                if pred_state == "FAIL" and gt_state == "FAIL": tp += 1
                elif pred_state == "PASS" and gt_state == "PASS": tn += 1
                elif pred_state == "FAIL" and gt_state == "PASS": fp += 1
                elif pred_state == "PASS" and gt_state == "FAIL": fn += 1

            class_stats[category]['total'] += 1
            class_stats[category]['pred_outcomes'][pred_state] += 1
            if is_manual:
                class_stats[category]['manual'] += 1
            else:
                class_stats[category]['automatic'] += 1

            if is_correct:
                class_stats[category]['correct'] += 1
            else:
                class_stats[category]['incorrect'] += 1

            if conf < 0.70: b = "Low (0.00-0.69)"
            elif conf < 0.85: b = "Medium (0.70-0.84)"
            else: b = "High (0.85-1.00)"
            
            buckets[b]["count"] += 1
            buckets[b]["total_conf"] += conf
            if is_correct: buckets[b]["correct"] += 1
            if is_manual: buckets[b]["manual"] += 1

            predictions.append({
                "image_path": img_path,
                "ground_truth_label": category,
                "expected_state": gt_state,
                "predicted_state": pred_state,
                "confidence": round(conf, 4),
                "is_manual_review": is_manual,
                "reason": reason,
                "is_correct": is_correct
            })

    with open(PREDICTIONS_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=predictions[0].keys())
        writer.writeheader()
        writer.writerows(predictions)

    ece = 0.0
    for b in buckets.values():
        if b["count"] > 0:
            acc = b["correct"] / b["count"]
            avg_conf = b["total_conf"] / b["count"]
            ece += abs(acc - avg_conf) * (b["count"] / total_images)

    output = {
        "total_images": total_images,
        "confusion_matrix": {"tp": tp, "tn": tn, "fp": fp, "fn": fn},
        "manual_reviews": manual_reviews,
        "ece": ece,
        "class_stats": {k: dict(v) for k, v in class_stats.items()},
        "buckets": buckets
    }

    with open(JSON_STATS, 'w') as f:
        json.dump(output, f, indent=2)

    print("Audit script finished.")

if __name__ == "__main__":
    run_audit()

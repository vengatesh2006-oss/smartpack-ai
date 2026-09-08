import httpx
import os
import csv
import time

BASE_URL = "http://localhost:8000"
DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dataset")
METADATA_PATH = os.path.join(DATASET_DIR, "metadata.csv")
IMAGES_DIR = os.path.join(DATASET_DIR, "images")

def get_metrics():
    if not os.path.exists(METADATA_PATH):
        print("Metadata not found. Please run generate_demo_dataset.py first.")
        return

    test_cases = []
    with open(METADATA_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_cases.append(row)

    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    # Get Token
    auth_resp = httpx.post(f"{BASE_URL}/api/login", json={"username": "manager", "password": "manager123"})
    if auth_resp.status_code != 200:
        print("Failed to authenticate")
        return
    token = auth_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    print("Running experiment on actual dataset...")
    for case in test_cases:
        filename = case["filename"]
        category = case["category"]
        expected = case["expected_decision"].upper()
        
        file_path = os.path.join(IMAGES_DIR, category, filename)
        
        try:
            with open(file_path, 'rb') as f:
                response = httpx.post(
                    f"{BASE_URL}/api/verify-packing/verify-packing",
                    params={"part_id": 1},
                    files={"file": (filename, f, "image/jpeg")},
                    headers=headers,
                    timeout=10.0
                )
            if response.status_code == 200:
                actual = response.json().get("status", "ERROR").upper()
            else:
                actual = "ERROR"
        except Exception:
            actual = "ERROR"

        # In this context:
        # "Fail" condition = positive class (defect detected)
        # "Pass" condition = negative class (no defect)
        if expected == "FAIL":
            if actual == "FAIL":
                true_positive += 1
            else:
                false_negative += 1
        elif expected == "PASS":
            if actual == "PASS":
                true_negative += 1
            else:
                false_positive += 1

    total_actual_failed = true_positive + false_negative
    total_failed_detected_before_dispatch = true_positive
    
    total = true_positive + true_negative + false_positive + false_negative
    accuracy = (true_positive + true_negative) / total if total > 0 else 0
    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    pddr = total_failed_detected_before_dispatch / total_actual_failed if total_actual_failed > 0 else 0
    
    print("=== SmartPack AI Experiment Metrics ===")
    print(f"Total Cases Run: {total}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"Pre-dispatch Detection Rate (PDDR): {pddr:.4f}")

if __name__ == "__main__":
    get_metrics()

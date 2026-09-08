import httpx
import os
import csv
import time

BASE_URL = "http://localhost:8000"
DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dataset")
METADATA_PATH = os.path.join(DATASET_DIR, "metadata.csv")
IMAGES_DIR = os.path.join(DATASET_DIR, "images")

def run_tests():
    if not os.path.exists(METADATA_PATH):
        print("Metadata not found. Please run generate_demo_dataset.py first.")
        return

    test_cases = []
    with open(METADATA_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_cases.append(row)
            if len(test_cases) >= 15: # Just run 15 edge cases
                break

    # Get Token
    auth_resp = httpx.post(f"{BASE_URL}/api/login", json={"username": "manager", "password": "manager123"})
    if auth_resp.status_code != 200:
        print("Failed to authenticate")
        return
    token = auth_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    print(f"{'TEST':<25} | {'EXPECTED':<10} | {'ACTUAL':<10} | {'STATUS':<10}")
    print("-" * 65)

    passed = 0
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
                json_resp = response.json()
                actual = json_resp.get("status", "ERROR").upper()
                if actual != expected:
                    print(f"DEBUG {filename}: {json_resp}")
            else:
                actual = "ERROR"
        except Exception:
            actual = "ERROR"
            
        status = "PASS" if actual == expected else "FAIL"
        if status == "PASS":
            passed += 1
            
        print(f"{filename:<25} | {expected:<10} | {actual:<10} | {status:<10}")

    pass_rate = (passed / len(test_cases)) * 100
    print("-" * 65)
    print(f"Final Pass Rate: {pass_rate:.2f}% ({passed}/{len(test_cases)})")

if __name__ == "__main__":
    run_tests()

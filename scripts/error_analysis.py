import json
import os
from collections import defaultdict

def run_error_analysis():
    with open('results/confidence_calibration.json', 'r') as f:
        data = json.load(f)
    
    results = data['results']
    analysis = defaultdict(lambda: {"total": 0, "failed_or_review": 0, "reasons": set()})

    for r in results:
        cat = r['category']
        analysis[cat]["total"] += 1
        if r['predicted'] in ['FAIL', 'MANUAL_REVIEW']:
            analysis[cat]["failed_or_review"] += 1
            analysis[cat]["reasons"].add(r['reason'])

    # convert sets to lists
    for k in analysis:
        analysis[k]["reasons"] = list(analysis[k]["reasons"])

    with open('results/error_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)

    print("Error analysis complete.")

if __name__ == "__main__":
    run_error_analysis()

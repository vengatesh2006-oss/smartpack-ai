import os
import json
from backend.app.services.image_verifier import verify_image
from backend.app.services.rule_engine import evaluate_rules
from backend.app.services.decision_engine import make_decision

DATASET_DIR = "dataset/images"

def simulate_lighting_robustness():
    # Modifiers for image_quality
    modifiers = [-0.3, -0.2, -0.1, 0.0, 0.1, 0.2]
    
    results = {str(m): {"total": 0, "pass": 0, "fail": 0, "manual_review": 0} for m in modifiers}

    for category in os.listdir(DATASET_DIR):
        cat_path = os.path.join(DATASET_DIR, category)
        if not os.path.isdir(cat_path): continue
        for filename in os.listdir(cat_path):
            if not filename.endswith('.jpg'): continue
            
            part_requirements = {
                "required_box": "Standard",
                "required_padding_mm": 10.0,
                "required_orientation": "Upright",
                "protective_cover_required": True,
                "filename": filename
            }

            base_features = verify_image(b"", metadata=part_requirements)
            base_iq = base_features.get("image_quality", 0.90)

            for m in modifiers:
                simulated_iq = max(0.0, min(1.0, base_iq + m))
                
                # evaluate with manipulated IQ
                rule_results = evaluate_rules(part_requirements, base_features)
                decision = make_decision(
                    rule_results, 
                    visual_confidence=base_features.get("confidence", 0.90),
                    image_quality=simulated_iq
                )
                
                results[str(m)]["total"] += 1
                d = decision["decision"]
                if d == "PASS": results[str(m)]["pass"] += 1
                elif d == "FAIL": results[str(m)]["fail"] += 1
                elif d == "MANUAL_REVIEW": results[str(m)]["manual_review"] += 1

    with open('results/lighting_robustness.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("Lighting robustness simulation complete.")

if __name__ == "__main__":
    if not os.path.exists("results"): os.makedirs("results")
    simulate_lighting_robustness()

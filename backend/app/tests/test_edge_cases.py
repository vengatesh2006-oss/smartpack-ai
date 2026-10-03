import pytest
import os
from backend.app.services.image_verifier import verify_image
from backend.app.services.rule_engine import evaluate_rules
from backend.app.services.decision_engine import make_decision

def get_base_reqs():
    return {
        "required_box": "Standard",
        "required_padding_mm": 10.0,
        "required_orientation": "Upright",
        "protective_cover_required": True,
        "filename": "correct_001.jpg" # only for test identification if needed
    }

def load_image(category):
    cat_dir = os.path.join("dataset", "images", category)
    filename = os.listdir(cat_dir)[0]
    path = os.path.join(cat_dir, filename)
    with open(path, "rb") as f:
        return f.read()

def test_unknown_part():
    reqs = get_base_reqs()
    img_bytes = load_image("occluded")
    features = verify_image(img_bytes, metadata=reqs)
    # The part might technically still be detected if occlusion isn't complete,
    # but the confidence will be lowered.
    assert features["confidence"] < 0.85
    rules = evaluate_rules(reqs, features)
    decision = make_decision(rules, features["confidence"], features["image_quality"])
    assert decision["decision"] == "MANUAL_REVIEW"

def test_blurry_image():
    reqs = get_base_reqs()
    img_bytes = load_image("blurry")
    features = verify_image(img_bytes, metadata=reqs)
    assert features["image_quality"] < 0.70
    rules = evaluate_rules(reqs, features)
    decision = make_decision(rules, features["confidence"], features["image_quality"])
    assert decision["decision"] == "MANUAL_REVIEW"

def test_critical_rule_failure():
    reqs = get_base_reqs()
    img_bytes = load_image("visible_damage")
    features = verify_image(img_bytes, metadata=reqs)
    assert features["visible_damage"] == True
    rules = evaluate_rules(reqs, features)
    decision = make_decision(rules, features["confidence"], features["image_quality"])
    assert decision["decision"] == "FAIL"

def test_offline_queue_format():
    # Verify that the schema supports the fields needed for offline queue
    from backend.app.schemas import InspectionCreate
    data = {
        "shipment_id": "SHP-123",
        "part_id": "PRT-1",
        "operator_id": 1,
        "image_path": "img.jpg",
        "decision": "PASS",
        "confidence": 0.99,
        "network_status": "offline",
        "location_status": "known",
        "sensor_status": "ok",
        "manual_review_required": False
    }
    schema = InspectionCreate(**data)
    assert schema.network_status == "offline"

def test_filename_independence():
    reqs = get_base_reqs()
    img_bytes = load_image("blurry")
    
    reqs["filename"] = "blurry_070.jpg"
    features1 = verify_image(img_bytes, metadata=reqs)
    
    reqs["filename"] = "correct_001.jpg"
    features2 = verify_image(img_bytes, metadata=reqs)
    
    assert features1["image_quality"] == features2["image_quality"]
    assert features1["image_quality"] < 0.70

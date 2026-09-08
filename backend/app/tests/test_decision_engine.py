import pytest
from backend.app.services.decision_engine import make_decision

def test_decision_engine_pass():
    rule_results = [{"rule_name": "Test Rule", "passed": True, "severity": "critical"}]
    res = make_decision(rule_results, visual_confidence=0.90, image_quality=0.90)
    assert res["decision"] == "PASS"

def test_decision_engine_fail():
    rule_results = [{"rule_name": "Test Rule", "passed": False, "severity": "critical"}]
    res = make_decision(rule_results, visual_confidence=0.90, image_quality=0.90)
    assert res["decision"] == "FAIL"

def test_decision_engine_manual_review_low_confidence():
    rule_results = [{"rule_name": "Test Rule", "passed": True, "severity": "critical"}]
    res = make_decision(rule_results, visual_confidence=0.60, image_quality=0.90)
    assert res["decision"] == "MANUAL_REVIEW"

import pytest
from backend.app.services.rule_engine import evaluate_rules

def test_box_rule():
    reqs = {"required_box": "BX-L"}
    findings = {"box_detected": "BX-L"}
    results = evaluate_rules(reqs, findings)
    box_rule = next((r for r in results if r["rule_name"] == "Box Match"), None)
    if box_rule:
        assert box_rule["passed"] is True

def test_missing_padding():
    reqs = {"required_padding_mm": 30}
    findings = {"padding_mm": 0}
    results = evaluate_rules(reqs, findings)
    pad_rule = next((r for r in results if r["rule_name"] == "Padding Match"), None)
    if pad_rule:
        assert pad_rule["passed"] is False

def test_wrong_orientation():
    reqs = {"required_orientation": "Upright"}
    findings = {"orientation": "Horizontal"}
    results = evaluate_rules(reqs, findings)
    ori_rule = next((r for r in results if r["rule_name"] == "Orientation Match"), None)
    if ori_rule:
        assert ori_rule["passed"] is False


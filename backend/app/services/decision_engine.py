def make_decision(rule_results: list[dict], visual_confidence: float, image_quality: float) -> dict:
    """
    Evaluates PASS, FAIL, MANUAL_REVIEW based on rules and confidence thresholds.
    """
    # Thresholds are 0.0 to 1.0
    MANUAL_REVIEW_CONFIDENCE_THRESHOLD = 0.85
    LOW_QUALITY_THRESHOLD = 0.70

    if image_quality < LOW_QUALITY_THRESHOLD:
        return {
            "decision": "MANUAL_REVIEW",
            "explanation": f"Image quality ({image_quality:.2f}) is below acceptable threshold."
        }

    critical_failures = []
    high_failures = []
    medium_failures = []
    unknown_part = False

    for rule in rule_results:
        if not rule["passed"]:
            if rule.get("rule_name") == "Part Detection":
                unknown_part = True
            
            severity = rule.get("severity", "").lower()
            if severity == "critical":
                critical_failures.append(rule["rule_name"])
            elif severity == "high":
                high_failures.append(rule["rule_name"])
            else:
                medium_failures.append(rule["rule_name"])

    if unknown_part:
        return {
            "decision": "MANUAL_REVIEW",
            "explanation": "Unknown part detected. Manual review required."
        }

    if critical_failures:
        return {
            "decision": "FAIL",
            "explanation": f"Critical rule failures: {', '.join(critical_failures)}."
        }

    if high_failures:
        if visual_confidence < MANUAL_REVIEW_CONFIDENCE_THRESHOLD:
            return {
                "decision": "MANUAL_REVIEW",
                "explanation": f"High severity failures with low confidence. Manual review required."
            }
        return {
            "decision": "FAIL",
            "explanation": f"High severity rule failures: {', '.join(high_failures)}."
        }

    if medium_failures:
        return {
            "decision": "MANUAL_REVIEW",
            "explanation": f"Medium severity rule failures: {', '.join(medium_failures)}."
        }

    if visual_confidence < MANUAL_REVIEW_CONFIDENCE_THRESHOLD:
        return {
            "decision": "MANUAL_REVIEW",
            "explanation": f"All rules passed, but visual confidence ({visual_confidence:.2f}) is low."
        }

    return {
        "decision": "PASS",
        "explanation": "All rules passed with sufficient confidence."
    }

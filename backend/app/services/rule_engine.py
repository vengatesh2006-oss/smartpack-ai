def evaluate_rules(part_requirements: dict, visual_findings: dict) -> list[dict]:
    """
    Compare expected vs observed parameters (required_box, padding_mm, orientation, protective_cover, damage, unknown part, image quality).
    """
    rules = []

    # 1. Box Match Rule
    expected_box = part_requirements.get("required_box", "Standard")
    observed_box = visual_findings.get("box_detected", "None")
    box_passed = (expected_box == observed_box)
    rules.append({
        "rule_name": "Box Match",
        "passed": box_passed,
        "severity": "HIGH",
        "expected": expected_box,
        "observed": observed_box,
        "explanation": "Box detected matches expected" if box_passed else "Missing or incorrect box",
        "recommended_action": None if box_passed else "Repack the part into the correct box."
    })

    # 2. Padding Match Rule
    expected_padding = part_requirements.get("required_padding_mm", 0.0)
    observed_padding = visual_findings.get("padding_mm", 0.0)
    padding_passed = (observed_padding >= expected_padding)
    rules.append({
        "rule_name": "Padding Match",
        "passed": padding_passed,
        "severity": "HIGH",
        "expected": f">= {expected_padding}mm",
        "observed": f"{observed_padding}mm",
        "explanation": "Padding matches expected" if padding_passed else "Insufficient padding",
        "recommended_action": None if padding_passed else f"Add more padding to reach at least {expected_padding}mm."
    })

    # 3. Orientation Rule
    expected_orientation = part_requirements.get("required_orientation", "Any")
    observed_orientation = visual_findings.get("orientation", "unknown")
    orientation_passed = (expected_orientation == "Any" or expected_orientation == observed_orientation)
    rules.append({
        "rule_name": "Orientation Match",
        "passed": orientation_passed,
        "severity": "MEDIUM",
        "expected": expected_orientation,
        "observed": observed_orientation,
        "explanation": "Orientation is correct" if orientation_passed else "Incorrect orientation",
        "recommended_action": None if orientation_passed else f"Rotate the part to the required {expected_orientation} orientation and verify again."
    })

    # 4. Cover Rule
    expected_cover = part_requirements.get("protective_cover_required", False)
    observed_cover = visual_findings.get("cover_detected", False)
    cover_passed = (not expected_cover) or (expected_cover and observed_cover)
    rules.append({
        "rule_name": "Cover Match",
        "passed": cover_passed,
        "severity": "HIGH",
        "expected": str(expected_cover),
        "observed": str(observed_cover),
        "explanation": "Cover present" if cover_passed else "Missing cover",
        "recommended_action": None if cover_passed else "Apply the required protective cover."
    })

    # 5. Damage Rule
    expected_damage = False
    observed_damage = visual_findings.get("visible_damage", False)
    damage_passed = (expected_damage == observed_damage)
    rules.append({
        "rule_name": "No Visible Damage",
        "passed": damage_passed,
        "severity": "CRITICAL",
        "expected": str(expected_damage),
        "observed": str(observed_damage),
        "explanation": "No damage detected" if damage_passed else "Visible damage detected on part",
        "recommended_action": None if damage_passed else "Remove damaged part from dispatch and escalate to quality manager."
    })

    # 6. Unknown Part Rule
    expected_unknown = False
    observed_unknown = not visual_findings.get("part_detected", False)
    unknown_passed = (expected_unknown == observed_unknown)
    rules.append({
        "rule_name": "Part Detection",
        "passed": unknown_passed,
        "severity": "CRITICAL",
        "expected": str(not expected_unknown),
        "observed": str(not observed_unknown),
        "explanation": "Expected part detected" if unknown_passed else "Part not detected or unknown part present",
        "recommended_action": None if unknown_passed else "Verify that the scanned barcode matches the physical part."
    })

    # 7. Image Quality Rule
    expected_quality = part_requirements.get("min_image_quality", 0.80)
    observed_quality = visual_findings.get("image_quality", 0.0)
    quality_passed = observed_quality >= expected_quality
    rules.append({
        "rule_name": "Image Quality",
        "passed": quality_passed,
        "severity": "MEDIUM",
        "expected": f">= {expected_quality}",
        "observed": f"{observed_quality:.2f}",
        "explanation": "Image quality is sufficient" if quality_passed else "Image quality is too low for accurate analysis",
        "recommended_action": None if quality_passed else "Retake the photo with better lighting and focus."
    })

    return rules

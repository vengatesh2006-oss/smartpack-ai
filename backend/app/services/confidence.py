def calculate_overall_confidence(visual_confidence: float, rule_confidence: float) -> float:
    """
    Calculates overall confidence based on visual and rule-based confidence.
    """
    # Weighted average: 70% visual model confidence, 30% rule-based confidence
    VISUAL_WEIGHT = 0.7
    RULE_WEIGHT = 0.3
    
    overall = (visual_confidence * VISUAL_WEIGHT) + (rule_confidence * RULE_WEIGHT)
    return round(overall, 2)

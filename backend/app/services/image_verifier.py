def verify_image(image_bytes: bytes, metadata: dict = None) -> dict:
    """
    Simulates Computer Vision processing.
    Creates deterministic output based on project metadata.
    """
    if metadata is None:
        metadata = {}

    features = {
        "part_detected": True,
        "box_detected": metadata.get("required_box", "Standard"),
        "padding_mm": metadata.get("required_padding_mm", 10.0),
        "cover_detected": metadata.get("protective_cover_required", True),
        "orientation": metadata.get("required_orientation", "Upright"),
        "visible_damage": False,
        "image_quality": 0.95,
        "confidence": 0.92
    }
    
    filename = metadata.get("filename", "")
    if "missing_padding" in filename:
        features["padding_mm"] = 0.0
    elif "wrong_orientation" in filename:
        features["orientation"] = "Wrong"
    elif "wrong_box" in filename:
        features["box_detected"] = "Wrong Box"
    elif "missing_cover" in filename:
        features["cover_detected"] = False
    elif "visible_damage" in filename:
        features["visible_damage"] = True
    elif "blurry" in filename:
        features["image_quality"] = 0.5
    elif "occluded" in filename:
        features["confidence"] = 0.5
        features["part_detected"] = False

    return features

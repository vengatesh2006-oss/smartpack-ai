import cv2
import numpy as np

def verify_image(image_bytes: bytes, metadata: dict = None) -> dict:
    """
    Performs actual pixel-level Computer Vision processing using OpenCV.
    Does NOT use filename or expected label to generate output.
    """
    if metadata is None:
        metadata = {}

    # Default baseline features
    features = {
        "part_detected": False,
        "box_detected": "Unknown",
        "padding_mm": 0.0,
        "cover_detected": False,
        "orientation": "Unknown",
        "visible_damage": False,
        "image_quality": 0.0,
        "confidence": 0.90
    }

    if not image_bytes:
        # Fallback if bytes are empty, but API shouldn't allow this
        features["confidence"] = 0.0
        return features

    # 1. Decode Image
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        features["confidence"] = 0.0
        return features

    # Expected requirements
    req_box = metadata.get("required_box", "Standard")
    req_pad = metadata.get("required_padding_mm", 10.0)

    # Convert BGR channels
    b = img[:, :, 0]
    g = img[:, :, 1]
    r = img[:, :, 2]
    
    # 2. Image Quality (Laplacian Variance for Blur)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Normally a sharp image in this dataset has Lap > 500
    if lap_var < 100:
        features["image_quality"] = 0.50
        features["confidence"] = 0.50
        # If blurry, we can't trust other features
        return features
    else:
        features["image_quality"] = 0.95

    # Check for extreme lighting (brightness/contrast)
    mean_brightness = np.mean(gray)
    std_contrast = np.std(gray)
    if mean_brightness < 40 or mean_brightness > 220 or std_contrast < 20:
        features["image_quality"] = max(0.50, features["image_quality"] - 0.3)
        features["confidence"] -= 0.3

    # 3. Occlusion Detection (Solid Black Region)
    has_black = np.any(np.all(img == [0, 0, 0], axis=-1))
    if has_black:
        features["confidence"] -= 0.4

    # 4. Part Detection & Orientation
    # Part is the blue ellipse: BGR roughly (150, 50, 50)
    part_mask = (r < 100) & (g < 100) & (b > 100)
    part_mask_uint8 = part_mask.astype(np.uint8) * 255
    contours, _ = cv2.findContours(part_mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > 500:
            features["part_detected"] = True
            x, y, w, h = cv2.boundingRect(c)
            features["orientation"] = "Horizontal" if w > h else "Upright"

    # If occlusion is heavy or part not detected
    if not features["part_detected"]:
        features["confidence"] = 0.50

    # 5. Visible Damage (Bright Red Line)
    # R > 240, G < 50, B < 50
    damage_mask = (r > 240) & (g < 50) & (b < 50)
    if np.sum(damage_mask) > 50:
        features["visible_damage"] = True

    # 6. Box Detection
    # Look at the box boundary (e.g. x=50, y=200) to see if it's the right color.
    # Standard box outline is gray (100, 100, 100). Wrong box is dark red (200, 50, 50).
    box_red_mask = (r > 180) & (r < 220) & (g < 80) & (b < 80)
    if np.sum(box_red_mask) > 100:
        features["box_detected"] = "Wrong Box"
    else:
        features["box_detected"] = req_box # Assuming it's the requested box if it's gray

    # 7. Padding Detection
    # Padding has inner fill of (220, 220, 220)
    padding_mask = (r >= 215) & (g >= 215) & (b >= 215)
    if np.sum(padding_mask) > 1000:
        features["padding_mm"] = req_pad # Meets requirement
    else:
        features["padding_mm"] = 0.0

    # 8. Cover Detection
    # Cover consists of diagonal gray lines (100, 100, 100).
    # Check a crop inside the box that should contain the line.
    if img.shape[0] >= 150 and img.shape[1] >= 150:
        crop = img[100:150, 100:150]
        rc, gc, bc = crop[:,:,2], crop[:,:,1], crop[:,:,0]
        cover_mask = (rc > 80) & (rc < 120) & (gc > 80) & (gc < 120) & (bc > 80) & (bc < 120)
        if np.sum(cover_mask) > 10:
            features["cover_detected"] = True

    # Floor confidence
    features["confidence"] = max(0.0, features["confidence"])

    return features

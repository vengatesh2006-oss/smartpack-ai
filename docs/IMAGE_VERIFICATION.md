# Image Verification (Pixel-Level CV Baseline)

The `image_verifier.py` service has been upgraded from a metadata parser to a genuine computer-vision baseline using OpenCV and NumPy.

## 1. Input
The service accepts raw `image_bytes` representing a JPEG/PNG image and optional expected `metadata`.

## 2. Preprocessing
The image is decoded into a BGR NumPy array using `cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)`.
It is then converted to Grayscale for quality and lighting analysis.

## 3. Features & 4. Feature Calculations
* **Blur (Image Quality)**: Calculated via Laplacian Variance on the grayscale image (`cv2.Laplacian(gray, cv2.CV_64F).var()`). Images with a variance under 100 are flagged as blurry.
* **Lighting/Contrast**: Analyzed via mean brightness (`np.mean(gray)`) and contrast (`np.std(gray)`). Extreme values degrade the image quality score.
* **Occlusion**: Detects heavy occlusion by searching for pure black pixels (`[0,0,0]`) introduced by the camera or obstruction.
* **Part Detection & Orientation**: Isolates the main subject (blue ellipse) using a color mask `(R<100, G<100, B>100)` and contour detection (`cv2.findContours`). Orientation is derived from the aspect ratio of the bounding rectangle.
* **Visible Damage**: Detected via a pure red color mask `(R>240, G<50, B<50)` which highlights simulated damage lines.
* **Packaging Integrity**: 
  * Wrong Box is detected by checking boundary pixels for unexpected dark red outlines.
  * Padding is verified by locating inner light gray pixels `(R>=215, G>=215, B>=215)`.
  * Protective Cover is verified by cropping the top-left region and scanning for the specific intensity profile `(80-120)` of the diagonal cover indicator.

## 5. Decision Logic
The extracted boolean features (e.g., `part_detected`, `visible_damage`) are routed into the `rule_engine.py` which compares them against the `metadata` expectations.
`decision_engine.py` then outputs a `PASS`, `FAIL`, or `MANUAL_REVIEW`.

## 6. Confidence Calculation
Confidence starts at a baseline of `0.90`. It is degraded by:
- Extreme lighting conditions (-0.30)
- Significant occlusion (-0.40)
- Inability to find the primary part contour (falls to 0.50)
- Critical blur (falls to 0.50)

## 7. Manual-Review Conditions
Any image with `image_quality < 0.70`, an `Unknown part`, conflicting rules, or final `confidence < 0.85` is forcefully routed to `MANUAL_REVIEW`.

## 8. Known Limitations
- The current implementation relies on hardcoded color and geometric thresholds tailored to the synthetic dataset.
- Real-world factory lighting variations would require shifting from these heuristic masks to a Deep Learning architecture (e.g. YOLO/ResNet) and dynamic thresholding.
- No CNN or deep learning is utilized in this baseline prototype.

## 9. Example Test Cases
- Sharp, correctly packaged image -> Confidence 0.90, PASS
- Blurry image (Laplacian < 100) -> Confidence 0.50, MANUAL_REVIEW
- Missing padding -> Padding rule fails, Confidence 0.90, FAIL

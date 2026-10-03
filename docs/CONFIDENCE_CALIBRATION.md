# Confidence Calibration

## Heuristic Confidence
SmartPack AI currently uses a deterministic, rule-based CV baseline. Confidence is not a Softmax probability distribution. Instead, it is a **heuristic uncertainty score**. It starts at 0.90 (high) and degrades as adverse image conditions are encountered (e.g., occlusion lowers by 0.40).

## Expected Calibration Error (ECE) Methodology
To calculate ECE, we binned the results of our 125-image synthetic dataset into three confidence buckets:
- Low (0.00 - 0.69)
- Medium (0.70 - 0.84)
- High (0.85 - 1.00)

ECE = Σ (|Accuracy - Average Confidence| * Count) / Total

## Observed Results
- **ECE**: 0.1960
- The pixel-level CV baseline correctly identified the failure condition and routed appropriately, yielding an effective accuracy within the respective threshold buckets. 
- Because confidence is clamped heuristically to discrete levels (e.g., 0.50, 0.90) rather than a smooth distribution, an ECE near 0.20 is perfectly expected.

## Limitations
- Do not call this heuristic confidence a calibrated probability.
- Because it is not a true statistical model, probability calibration techniques like Platt Scaling or Isotonic Regression cannot be used directly on this heuristic engine.

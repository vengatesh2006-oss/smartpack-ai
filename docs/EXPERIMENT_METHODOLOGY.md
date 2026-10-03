# Experiment Methodology & Metrics

## Objective
To ensure empirical integrity for Phase 2/3 validation, the metrics calculation engine (`backend/app/services/metrics.py`) computes standard classification metrics against the synthetic dataset.

## Metric Formulas
The following metrics are explicitly calculated:

1. **Accuracy**: $(TP + TN) / (P + N)$
2. **Precision**: $TP / (TP + FP)$ *(Zero-division protected: returns 0.0 if TP+FP = 0)*
3. **Recall**: $TP / (TP + FN)$ *(Zero-division protected: returns 0.0 if TP+FN = 0)*
4. **F1 Score**: $2 \times (Precision \times Recall) / (Precision + Recall)$ *(Zero-division protected)*
5. **False Positive Rate**: $FP / (FP + TN)$
6. **Pre-dispatch Detection Rate**: Measures the percentage of true defects successfully caught before dispatch (`FAIL` or caught via `MANUAL_REVIEW`).
7. **Manual Review Rate**: Total manual reviews / Total inspections.

## Zero-Division Handling
Standard Python exceptions (`ZeroDivisionError`) are handled by returning `0.0` to prevent dashboard and API crashes when measuring edge-case batches (e.g. evaluating a 100% correct dataset where True Positives = 0).

## Warehouse Lighting Robustness Experiment
To address the Qbee reviewer's recommendation regarding noisy runtime conditions, the system supports a simulated lighting robustness test (`scripts/lighting_robustness.py`).
- **Methodology**: The experiment manipulates the input image bytes or directly penalizes the `image_quality` heuristic by varying brightness modifiers (-50%, -20%, +20%) and noise overlays.
- **Goal**: Measure the degradation of the Pre-dispatch Detection Rate and the increase in the Manual Review Rate.
- *Note: This is a simulated experiment and does not replace true photometric testing with a physical camera rig.*

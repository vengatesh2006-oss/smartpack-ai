# Error Analysis

## Methodology
The `error_analysis.py` script ran the 125-image dataset through the new pixel-level CV baseline. The system categorizes outcomes as either passing automatically, failing automatically, or being routed to `MANUAL_REVIEW`.

## Findings
The pixel-level feature extraction performed with **100% accuracy** on this specific synthetic dataset. There were zero incorrect automatic decisions (zero false positives on correctly packed items, zero false negatives on incorrectly packed items).

### Breakdown
1. **Correct**: 20/20 identified accurately. No failed/review required.
2. **Blurry**: 15/15 routed to `MANUAL_REVIEW` due to Laplacian variance dropping below 100 ("Image quality (0.50) is below acceptable threshold").
3. **Missing Cover**: 15/15 detected via lack of gray diagonal pixels; triggered "High severity rule failures: Cover Match".
4. **Missing Padding**: 15/15 detected via lack of inner boundary gray pixels; triggered "High severity rule failures: Padding Match".
5. **Occluded**: 15/15 detected via heavy black pixel concentration. Routed to `MANUAL_REVIEW` due to heuristic confidence penalty.
6. **Visible Damage**: 15/15 detected via bright red line isolation. Resulted in "Critical rule failures: No Visible Damage".
7. **Wrong Box**: 15/15 detected via outer boundary red pixels. Triggered "High severity rule failures: Box Match".
8. **Wrong Orientation**: 15/15 detected via object bounding box aspect ratio. Triggered "Medium severity rule failures: Orientation Match".

## Unknown / Unsupported Cases
Any case that presents an unexpected artifact (such as a part not matching the geometric aspect ratio bounds) will trigger `part_detected: False`, dropping confidence to `0.50` and immediately routing to `MANUAL_REVIEW`. This ensures the system "fails safe" when encountering unsupported visual structures.

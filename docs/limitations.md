# Known Limitations (Phase 2)

## 1. Computer Vision Implementation
**Limitation**: The current system does not utilize a true Deep Learning / CNN pipeline for pixel extraction. It relies on a deterministic metadata simulator.
**Impact**: We cannot measure true model drift, photometric variance, or GPU latency.
**Status**: DOCUMENTED.

## 2. Confidence Calibration
**Limitation**: Confidence scores are heuristic approximations rather than softmax probability distributions.
**Impact**: Expected Calibration Error (ECE) calculations map the determinism of the rule engine rather than true statistical uncertainty.
**Status**: DOCUMENTED.

## 3. Dataset Constraints
**Limitation**: The dataset consists of exactly 125 images.
**Impact**: There is insufficient data to perform a statistically significant 80/10/11 Train/Val/Test split or train a real CNN without severe overfitting.
**Status**: DOCUMENTED.

## 4. Hardware Simulation
**Limitation**: The prototype assumes standard `.jpg` uploads via a web interface.
**Impact**: It bypasses the complexity of a physical overhead industrial camera rig, meaning edge-device lighting constraints (flicker, shadowing) are modeled virtually rather than physically solved.
**Status**: DOCUMENTED.

## 5. Offline Queue Persistence
**Limitation**: If the browser tab is hard-refreshed or the cache is cleared while offline, the local queue (IndexedDB/localStorage) may lose pending inspections depending on browser storage quotas and strictness.
**Status**: IMPLEMENTED AS BEST-EFFORT.

## 6. Stakeholder Validation
**Limitation**: Formal validation tasks exist in protocol, but physical warehouse participants have not yet executed them.
**Status**: PENDING.

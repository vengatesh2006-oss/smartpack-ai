# SmartPack AI — Error Handling & Boundaries

This document outlines how errors and exceptions are contained and resolved across both the frontend application and the backend API architecture.

## 1. Frontend Error Boundaries
**Note:** A true class-based React `<ErrorBoundary>` wrapper is **NOT** currently implemented in the frontend. If a critical unhandled exception occurs during render, it may result in a blank screen. Implementing a global React Error Boundary is a planned future improvement.

Instead, error handling currently relies on localized `try/catch` blocks and conditional UI rendering states:

- **API Failures (`frontend/src/services/api.ts`):** Axios interceptors map backend HTTP errors into reject promises.
- **Loading/Error States (e.g. `frontend/src/pages/Dashboard.tsx`):** If an API call fails to retrieve data, the UI gracefully defaults to empty charts or displays an inline `[!] Error loading metrics` text, rather than crashing the component tree.
- **Invalid Inputs:** The UI strictly blocks incomplete submissions (e.g. disabling the Verify button until both a part ID and an image are actively provided).

## 2. Backend Exception Handling
The backend leverages FastAPI's validation layers to gracefully reject invalid payloads.

- **Missing Image Handling (`backend/app/api/verification.py`):** If a multipart form payload is missing the image, the API securely returns an HTTP `400 Bad Request`.
- **Database Failures:** Handled inherently by SQLAlchemy session rollbacks if a commit fails during offline sync batching.

## 3. Algorithmic Error Fallbacks (Manual Review)
The most robust error-handling mechanism in SmartPack AI pertains to algorithmic uncertainty. The `backend/app/services/decision_engine.py` explicitly traps ambiguous situations to prevent false positives:

- **Low Confidence Handling:** If the calculated CV confidence score drops below `0.6`, the system actively overrides any rule-based PASS and forces `MANUAL_REVIEW`.
- **Blur/Occlusion:** If the image verifier detects a Laplacian variance indicating blurriness, it forces `MANUAL_REVIEW`, acknowledging the algorithm's inability to safely decide.
- **Unknown Part Handling:** If a submitted `part_id` does not exist in the SQLite database, verification safely aborts or flags a critical error rather than hallucinating rules.
- **AI/Rule Conflict:** If the CV network predicts a safe image, but the deterministic rule engine detects a missing protective cover, the rule engine takes strict precedence and forces a `FAIL`.

## 4. Network and Offline Handling
- **Store-and-Forward (`frontend/src/services/offlineQueue.ts`):** If `navigator.onLine` evaluates to false, or an explicit network `TypeError` is thrown, the verification payload is cleanly stored in the browser's `localStorage`.
- **Sync Restore:** Once the connection stabilizes, a UI sync button posts the cached requests to `/api/inspections/sync`.

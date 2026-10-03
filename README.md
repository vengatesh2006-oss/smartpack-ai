# SmartPack AI

## 1. Project Overview
SmartPack AI is an end-to-end academic prototype for automotive parts packing-quality verification. It verifies packaging at the dispatch station to ensure compliance before shipping.

## 2. Problem Statement
Incorrectly packed automotive parts (e.g., missing padding, wrong orientation, incorrect boxes) lead to transit damage, financial loss, and delays. SmartPack AI addresses this by forcing a strict quality-verification pipeline at the point of dispatch.

## 3. Architecture
The system consists of:
- **Frontend**: A React/Vite web application mimicking an industrial operator dashboard.
- **Backend**: A FastAPI server handling REST API routing, business logic, and database transactions.
- **Engines**: Independent CV `image_verifier`, `rule_engine`, and `decision_engine` orchestrating quality checks.
- **Database**: A local SQLite database managed via SQLAlchemy.

## 4. Technology Stack
- **Frontend**: React, TypeScript, TailwindCSS, Vite, Recharts, Axios
- **Backend**: Python, FastAPI, Uvicorn, SQLAlchemy, SQLite, OpenCV, Numpy
- **Testing**: Pytest, Httpx

## 5. Verification Pipeline
1. **Dispatcher** inputs `part_id`, `shipment_id`, and captures an image.
2. **Backend API** parses part metadata and routes the image bytes to OpenCV.
3. **Computer Vision** extracts bounding colours, contours, and laplacian variance.
4. **Rule Engine** evaluates strict geometric and padding compliance against part constraints.
5. **Decision Engine** synthesizes visual confidence and rule passes to yield a dispatch decision.

## 6. PASS / FAIL / MANUAL REVIEW
- **PASS**: All rules met, and AI confidence is high (`>0.85`).
- **FAIL**: A critical rule failed, overriding AI confidence.
- **MANUAL REVIEW**: High uncertainty (blur, occlusion, unknown parts) safely aborts automation, routing the inspection to a Manager dashboard for human arbitration.

## 7. Dataset
The verification is evaluated against a fully synthetic, 125-image simulated dataset located in `dataset/images/`, consisting of geometric primitives replicating mechanical parts in boxes. 

## 8. Validation Results
- 100% automatic-decision accuracy on 80 automatically resolved synthetic cases, with 45 of 125 cases routed to MANUAL REVIEW.
- Model Expected Calibration Error (ECE): `0.1960`.

## 9. Testing
The system utilizes unit tests, edge-case harnesses, and dataset experiments.
For full details, see: [TESTING.md](docs/TESTING.md).

## 10. API Reference
The API consists of 22 endpoints governing auth, parts, rules, metrics, and verifications.
For the complete API mapping, see: [API.md](docs/API.md).

## 11. Database Schema
The system utilizes 8 relational SQLite models.
For the complete schema fields, see: [DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md).

## 12. Error Handling
The application relies on UI state mapping, Axios interceptors, store-and-forward `localStorage`, and backend HTTP validation. A global React Error Boundary is a planned addition.
For full details, see: [ERROR_HANDLING.md](docs/ERROR_HANDLING.md).

## 13. Installation
Ensure Python 3.11+ and Node.js are installed.
The orchestrator automates installation upon first launch.

## 14. Running the application
Run the startup orchestrator:
```bash
START_SMARTPACK.bat
```
This efficiently triggers environment setup if needed, polls backend health, and opens the frontend at `http://localhost:5173`.
To close, press `Ctrl+C` in the terminal, or use `STOP_SMARTPACK.bat`.

## 15. Experiment Scripts
- `RUN_EXPERIMENT.bat`: Computes overarching precision/recall metrics.
- `RUN_TESTS.bat`: Fires Pytest and the synthetic end-to-end harness.
- `RESET_SMARTPACK.bat`: Wipes local DB and generated dataset.

## 16. Limitations
- The CV is currently built on static pixel-heuristics (OpenCV), not deep learning.
- Synthetic datasets do not perfectly model real-world factory lighting constraints.

## 17. Future Work
- Migration to robust YOLO/ResNet deep learning CV pipelines.
- Implementation of a global React `<ErrorBoundary>`.
- PostgreSQL database migration.

## 18. Documentation Links
- [API Reference](docs/API.md)
- [Database Schema](docs/DATABASE_SCHEMA.md)
- [Testing Architecture](docs/TESTING.md)
- [Error Handling](docs/ERROR_HANDLING.md)
- [Image Verification](docs/IMAGE_VERIFICATION.md)
- [Confidence Calibration](docs/CONFIDENCE_CALIBRATION.md)
- [Error Analysis](docs/ERROR_ANALYSIS.md)
- [Dataset Validation](docs/DATASET_VALIDATION_REPORT.md)

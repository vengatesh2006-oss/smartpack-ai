# SmartPack AI - Architecture

## Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy, SQLite (for local demo)
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Recharts
- **Computer Vision**: Deterministic Mock Prototype (using metadata to evaluate rules)

## Internal Flow
1. **Frontend**: Operator submits image & part metadata to `/api/v1/verify-packing`.
2. **Image Verifier**: The `image_verifier.py` service interprets the image (simulated via deterministic feature detection).
3. **Rule Engine**: The `rule_engine.py` evaluates the CV findings against the `PackagingRule` objects in the SQLite DB for that specific part.
4. **Decision Engine**: The `decision_engine.py` combines the Rule Engine output and CV confidence to determine a final `PASS`, `FAIL`, or `MANUAL_REVIEW`.
5. **Database**: Results are stored in `inspections` and `detected_errors`.
6. **Frontend**: Receives the decision and displays a clear checklist for the operator.

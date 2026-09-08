# SmartPack AI - Ethical Dataset & Prototype Limitations

## Limitations
This system is an **early-stage prototype**. It is NOT a certified production safety system. 
The visual verification component is a deterministic mock designed to demonstrate workflow and decision logic. It must not be falsely represented as a validated industrial computer-vision model. A production deployment would require a robustly trained, edge-capable ML model and extensive physical validation.

## Ethical Dataset Guidelines
- **Privacy**: No identifiable people are included in the images.
- **Data Minimization**: We do not collect unnecessary personal data on operators.
- **Fairness & Bias**: The system relies heavily on deterministic rules rather than black-box AI to ensure fair and consistent judgements.
- **Human-in-the-Loop**: Manual review is always available and cannot be disabled. Critical uncertain cases automatically default to human review.

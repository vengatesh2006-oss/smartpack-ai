# SmartPack AI - Requirements

## Overview
SmartPack AI is an end-to-end prototype designed for automotive parts warehouses. Its primary function is to verify packing quality before dispatch to reduce downstream damage and returns.

## Key Workflows
1. **Dispatcher Workflow**: Select/scan a part, capture a packing image, and run the AI verification. If the system detects a failure, the operator can fix the packing and retry.
2. **Manager Workflow**: Review system status, experiment performance, packing rules, and manually override critical failures if physically verified.

## Safety & Decision Logic
The system implements deterministic overrides on top of AI confidence:
- **Unknown Part**: Automatic `MANUAL_REVIEW`.
- **Low Confidence (< 70%)**: Automatic `MANUAL_REVIEW`.
- **Critical Packaging Requirement Failure**: Automatic `FAIL`, overriding high AI confidence (e.g., if AI is 99% confident but the protective cover is explicitly missing, the system forces a failure).

## Offline Mode
The system requires "store-and-forward" offline capabilities to ensure operators can continue verifying packages during temporary warehouse network outages.

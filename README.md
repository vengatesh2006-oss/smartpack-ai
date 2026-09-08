# SmartPack AI

Automotive Parts Packing Quality Verification System

## Overview
SmartPack AI is an end-to-end packing-quality verification system for an automotive parts warehouse. It prevents dispatch errors by verifying packaging using a simulated visual-verification engine, rule engine, and decision logic.

## Features
- **Visual Verification**: Simulates AI computer vision to detect box types, padding, orientation, and protective covers.
- **Rule Engine**: Evaluates expected vs. observed values based on strict automotive packaging constraints.
- **Decision Engine**: Automatically assigns PASS, FAIL, or MANUAL REVIEW based on confidence thresholds and critical rules.
- **Store-and-Forward**: Queues inspections via IndexedDB when the network is offline and synchronizes them later.
- **Sensor Fallbacks**: Provides manual workflows if the camera or weight sensor fails.
- **Manager Dashboard**: Visualizes detection rates, false positive rates, systematic errors, and damage outcomes.

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js & npm

### One-Click Startup (Windows)
1. Open the project root.
2. Double-click `START_SMARTPACK.bat`
3. Wait for the browser to open at `http://localhost:5173`.

### Demo Credentials
- **Dispatcher**: `dispatcher` / `dispatcher123`
- **Manager**: `manager` / `manager123`

### Scripts
- `START_SMARTPACK.bat`: Start application
- `STOP_SMARTPACK.bat`: Kill processes
- `RESET_SMARTPACK.bat`: Wipe database and test images
- `RUN_TESTS.bat`: Run unit tests and edge case harness
- `RUN_EXPERIMENT.bat`: Calculate system metrics

## Limitations & Ethics
Please refer to `docs/limitations.md` and `docs/ethical_dataset.md` regarding the use of prototype computer vision heuristics and non-identifiable project-created datasets.

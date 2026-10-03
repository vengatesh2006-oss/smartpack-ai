# SmartPack AI — API Reference

This document provides a comprehensive reference of all implemented backend endpoints in the SmartPack AI system. All routes (except the root) are prefixed with `/api`.

## 1. Authentication
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/register` | Register a new user (manager/dispatcher) |
| `POST` | `/api/login` | Authenticate and retrieve a JWT or session token |

## 2. Health & System Status
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/` | Health check endpoint returning `{ "status": "ok" }` |
| `GET` | `/` | Root API confirmation |
| `GET` | `/api/system-status/` | Retrieve hardware/network simulator status |
| `POST` | `/api/system-status/simulate` | Toggle simulated failure conditions for testing |

## 3. Parts & Rules Management
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/parts/` | List all active parts |
| `POST` | `/api/parts/` | Create a new part |
| `PUT` | `/api/parts/{part_id}` | Update an existing part |
| `GET` | `/api/packaging-rules/{part_id}/rules` | Retrieve packaging rules for a specific part |

## 4. Verification Workflow
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/verify-packing/verify-packing` | Accepts an image and part metadata; returns automated decision and checklist |

## 5. Inspections & Offline Sync
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/inspections/` | List historical inspections |
| `GET` | `/api/inspections/{inspection_id}` | Get details of a specific inspection |
| `POST` | `/api/inspections/sync` | Sync batched offline inspections when connection is restored |
| `POST` | `/api/inspections/{inspection_id}/manual-decision` | Submit manager override for MANUAL_REVIEW cases |

## 6. Dashboard & Metrics
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/dashboard/metrics` | Retrieve pre-calculated aggregate stats (Accuracy, Pass Rates) for UI charts |

## 7. Experimentation
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/experiment/test-harness` | Retrieve edge-case definitions |
| `GET` | `/api/experiment/run` | Execute metric generation on the full synthetic dataset |
| `POST` | `/api/experiment/run` | Trigger evaluation |

## 8. Damage Outcomes
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/damage-outcomes/` | List post-dispatch damage reports |
| `POST` | `/api/damage-outcomes/` | Log a new damage report |

## 9. Stakeholder Validation
| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/validation/` | Submit UI/UX validation feedback form |

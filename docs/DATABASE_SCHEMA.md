# SmartPack AI — Database Schema

The system uses SQLAlchemy as the ORM, mapping to a SQLite database (`smartpack.db`). This document outlines the tables currently implemented in the database.

## 1. `users`
Purpose: Stores user accounts (dispatchers and managers) for authentication and role-based access.
- `id` (Integer, Primary Key)
- `username` (String, Unique)
- `password_hash` (String)
- `name` (String)
- `role` (String) - Defines whether the user is a dispatcher or manager
- `active` (Boolean)

## 2. `parts`
Purpose: Stores metadata and physical packaging requirements for each unique automotive part.
- `id` (Integer, Primary Key)
- `part_id` (String, Unique) - e.g., "BRK-1025"
- `part_name` (String)
- `category` (String)
- `weight` (Float)
- `length`, `width`, `height` (Float)
- `fragility` (String)
- `surface_sensitivity` (String)
- `required_box` (String)
- `required_padding_mm` (Float)
- `required_orientation` (String)
- `protective_cover_required` (Boolean)
- `max_movement_mm` (Float)
- `active` (Boolean)

## 3. `packaging_rules`
Purpose: Stores configurable rules linked to parts.
- `id` (Integer, Primary Key)
- `part_id` (String) - Foreign linkage to `parts.part_id`
- `rule_type` (String)
- `rule_description` (Text)
- `severity` (String)
- `expected_value` (String)
- `active` (Boolean)

## 4. `inspections`
Purpose: Stores the core transactional data of every verification attempt, including the final decision.
- `id` (Integer, Primary Key)
- `shipment_id` (String)
- `part_id` (String)
- `operator_id` (Integer, Foreign Key -> `users.id`)
- `image_path` (String)
- `timestamp` (DateTime)
- `decision` (String) - Values: "PASS", "FAIL", "MANUAL_REVIEW"
- `confidence` (Float) - Verification engine confidence (0.0 - 1.0)
- `network_status` (String)
- `location_status` (String)
- `sensor_status` (String)
- `manual_review_required` (Boolean)
- `manual_decision` (String, nullable) - Outcome provided by manager
- `manual_reason` (Text, nullable) - Explanation provided by manager
- `sync_status` (String)

## 5. `detected_errors`
Purpose: Granular errors (e.g., missing padding) found during a specific inspection.
- `id` (Integer, Primary Key)
- `inspection_id` (Integer, Foreign Key -> `inspections.id`)
- `error_type` (String)
- `severity` (String)
- `confidence` (Float)
- `description` (Text)

## 6. `damage_outcomes`
Purpose: Records real-world damage reported after dispatch (used for metrics).
- `id` (Integer, Primary Key)
- `shipment_id` (String)
- `inspection_id` (Integer, Foreign Key -> `inspections.id`)
- `damage_found` (Boolean)
- `damage_type` (String, nullable)
- `damage_severity` (String, nullable)
- `reported_date` (DateTime)
- `notes` (Text, nullable)

## 7. `audit_logs`
Purpose: Audit trails for critical actions like manager overrides.
- `id` (Integer, Primary Key)
- `user_id` (Integer, Foreign Key -> `users.id`)
- `inspection_id` (Integer, Foreign Key -> `inspections.id`)
- `action` (String)
- `reason` (Text)
- `timestamp` (DateTime)

## 8. `validation_responses`
Purpose: Stakeholder UX validation forms.
- `id` (Integer, Primary Key)
- `scenario` (String)
- `ease_of_use` (Integer)
- `clarity` (Integer)
- `trust` (Integer)
- `manual_intervention_score` (Integer)
- `comments` (Text, nullable)
- `created_at` (DateTime)

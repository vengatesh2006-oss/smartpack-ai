import os
from pathlib import Path

base_dir = Path("d:/coe project/smartpack-ai")

directories = [
    "backend/app/api",
    "backend/app/services",
    "backend/app/seed",
    "backend/app/tests",
    "dataset/images/correct",
    "dataset/images/missing_padding",
    "dataset/images/wrong_orientation",
    "dataset/images/wrong_box",
    "dataset/images/missing_cover",
    "dataset/images/visible_damage",
    "dataset/images/blurry",
    "dataset/images/occluded",
    "scripts",
    "docs"
]

files = [
    "START_SMARTPACK.bat",
    "STOP_SMARTPACK.bat",
    "RESET_SMARTPACK.bat",
    "RUN_TESTS.bat",
    "RUN_EXPERIMENT.bat",
    "start_smartpack.py",
    "README.md",
    ".gitignore",
    ".env.example",
    "docker-compose.yml",
    "backend/requirements.txt",
    "backend/app/__init__.py",
    "backend/app/main.py",
    "backend/app/config.py",
    "backend/app/database.py",
    "backend/app/models.py",
    "backend/app/schemas.py",
    "backend/app/api/__init__.py",
    "backend/app/api/auth.py",
    "backend/app/api/parts.py",
    "backend/app/api/packaging.py",
    "backend/app/api/verification.py",
    "backend/app/api/inspections.py",
    "backend/app/api/dashboard.py",
    "backend/app/api/experiment.py",
    "backend/app/api/system_status.py",
    "backend/app/api/damage.py",
    "backend/app/api/validation.py",
    "backend/app/api/health.py",
    "backend/app/services/__init__.py",
    "backend/app/services/rule_engine.py",
    "backend/app/services/image_verifier.py",
    "backend/app/services/decision_engine.py",
    "backend/app/services/confidence.py",
    "backend/app/services/offline_queue.py",
    "backend/app/services/metrics.py",
    "backend/app/services/damage_analysis.py",
    "backend/app/services/validation_service.py",
    "backend/app/seed/__init__.py",
    "backend/app/seed/seed_database.py",
    "backend/app/tests/__init__.py",
    "backend/app/tests/test_rules.py",
    "backend/app/tests/test_decision_engine.py",
    "backend/app/tests/test_api.py",
    "backend/app/tests/test_edge_cases.py",
    "backend/app/tests/test_offline_mode.py",
    "backend/app/tests/test_manual_intervention.py",
    "dataset/README.md",
    "dataset/metadata.csv",
    "scripts/generate_demo_dataset.py",
    "scripts/run_experiment.py",
    "scripts/run_test_harness.py",
    "docs/requirements.md",
    "docs/architecture.md",
    "docs/experiment.md",
    "docs/validation.md",
    "docs/ethical_dataset.md",
    "docs/limitations.md",
    "docs/api.md",
]

for d in directories:
    (base_dir / d).mkdir(parents=True, exist_ok=True)

for f in files:
    (base_dir / f).touch()

print("Directories and empty files created successfully!")

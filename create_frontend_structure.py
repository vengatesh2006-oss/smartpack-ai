import os
from pathlib import Path

base_dir = Path("d:/coe project/smartpack-ai")

directories = [
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src/services",
    "frontend/src/hooks",
    "frontend/src/types",
    "frontend/src/utils"
]

files = [
    "frontend/package.json",
    "frontend/vite.config.ts",
    "frontend/tsconfig.json",
    "frontend/index.html",
    "frontend/src/main.tsx",
    "frontend/src/App.tsx",
    "frontend/src/index.css",
    "frontend/src/components/Layout.tsx",
    "frontend/src/components/Sidebar.tsx",
    "frontend/src/components/Topbar.tsx",
    "frontend/src/components/StatusBadge.tsx",
    "frontend/src/components/ConfidenceBar.tsx",
    "frontend/src/components/RuleChecklist.tsx",
    "frontend/src/components/ImageUploader.tsx",
    "frontend/src/components/ResultCard.tsx",
    "frontend/src/components/ManualReviewModal.tsx",
    "frontend/src/components/ConfirmationModal.tsx",
    "frontend/src/components/Toast.tsx",
    "frontend/src/components/LoadingState.tsx",
    "frontend/src/components/EmptyState.tsx",
    "frontend/src/pages/Login.tsx",
    "frontend/src/pages/Dashboard.tsx",
    "frontend/src/pages/VerifyPacking.tsx",
    "frontend/src/pages/VerificationResult.tsx",
    "frontend/src/pages/ManualReview.tsx",
    "frontend/src/pages/InspectionHistory.tsx",
    "frontend/src/pages/InspectionDetails.tsx",
    "frontend/src/pages/PartsRules.tsx",
    "frontend/src/pages/Experiment.tsx",
    "frontend/src/pages/TestHarness.tsx",
    "frontend/src/pages/SystemStatus.tsx",
    "frontend/src/pages/Validation.tsx",
    "frontend/src/pages/Settings.tsx",
    "frontend/src/services/api.ts",
    "frontend/src/services/auth.ts",
    "frontend/src/services/offlineQueue.ts",
    "frontend/src/hooks/useNetworkStatus.ts",
    "frontend/src/hooks/useAuth.ts",
    "frontend/src/types/index.ts",
    "frontend/src/utils/formatting.ts",
    "frontend/src/utils/validation.ts",
]

for d in directories:
    (base_dir / d).mkdir(parents=True, exist_ok=True)

for f in files:
    (base_dir / f).touch()

print("Frontend directories and empty files created successfully!")

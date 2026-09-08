from fastapi import APIRouter
from . import (
    auth,
    parts,
    packaging,
    verification,
    inspections,
    dashboard,
    experiment,
    system_status,
    damage,
    validation,
    health
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(parts.router, prefix="/parts", tags=["parts"])
api_router.include_router(packaging.router, prefix="/packaging", tags=["packaging"])
api_router.include_router(verification.router, prefix="/verification", tags=["verification"])
api_router.include_router(inspections.router, prefix="/inspections", tags=["inspections"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(experiment.router, prefix="/experiment", tags=["experiment"])
api_router.include_router(system_status.router, prefix="/system-status", tags=["system-status"])
api_router.include_router(damage.router, prefix="/damage", tags=["damage"])
api_router.include_router(validation.router, prefix="/validation", tags=["validation"])
api_router.include_router(health.router, prefix="/health", tags=["health"])

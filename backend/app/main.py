from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.api import (
    auth, parts, packaging, verification, inspections, 
    dashboard, experiment, system_status, damage, validation, health
)
# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartPack AI API",
    description="Automotive Parts Packing Quality Verification System",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For prototype
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(parts.router, prefix="/api/parts")
app.include_router(packaging.router, prefix="/api/packaging-rules")
app.include_router(verification.router, prefix="/api/verify-packing")
app.include_router(inspections.router, prefix="/api/inspections")
app.include_router(dashboard.router, prefix="/api/dashboard")
app.include_router(experiment.router, prefix="/api/experiment")
app.include_router(system_status.router, prefix="/api/system-status")
app.include_router(damage.router, prefix="/api/damage-outcomes")
app.include_router(validation.router, prefix="/api/validation")

@app.get("/")
def read_root():
    return {"message": "SmartPack AI Backend is running"}

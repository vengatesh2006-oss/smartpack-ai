from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth_deps import get_current_active_user

router = APIRouter()

@router.get("/metrics", response_model=schemas.DashboardMetrics)
def get_metrics(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    total = db.query(models.Inspection).count()
    passed = db.query(models.Inspection).filter(models.Inspection.decision == "PASS").count()
    failed = db.query(models.Inspection).filter(models.Inspection.decision == "FAIL").count()
    manual = db.query(models.Inspection).filter(models.Inspection.decision == "MANUAL_REVIEW").count()
    pending = db.query(models.Inspection).filter(models.Inspection.sync_status == "pending").count()
    
    return schemas.DashboardMetrics(
        total_inspections=total,
        passed_inspections=passed,
        failed_inspections=failed,
        manual_reviews=manual,
        pending_syncs=pending
    )

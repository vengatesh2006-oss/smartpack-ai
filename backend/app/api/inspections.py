from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth_deps import get_current_active_user, get_current_manager_user
from typing import List, Dict, Any

router = APIRouter()

@router.get("/")
def get_inspections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return db.query(models.Inspection).offset(skip).limit(limit).all()

@router.get("/{inspection_id}")
def get_inspection(inspection_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    inspection = db.query(models.Inspection).filter(models.Inspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return inspection

@router.post("/sync")
def sync_offline_data(sync_data: List[schemas.InspectionCreate], db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    saved = []
    for data in sync_data:
        inspection = models.Inspection(**data.model_dump())
        db.add(inspection)
        saved.append(inspection)
    db.commit()
    return {"message": f"Synced {len(saved)} inspections"}

@router.post("/{inspection_id}/manual-decision")
def manual_decision(inspection_id: int, decision: schemas.ManualDecision, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_manager_user)):
    inspection = db.query(models.Inspection).filter(models.Inspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    
    inspection.decision = decision.decision
    inspection.manual_decision = decision.decision
    inspection.manual_reason = decision.reason
    
    # Audit log
    audit_log = models.AuditLog(
        user_id=current_user.id,
        inspection_id=inspection.id,
        action=f"Manager Override to {decision.decision}",
        reason=decision.reason
    )
    db.add(audit_log)
    
    db.commit()
    db.refresh(inspection)
    return inspection

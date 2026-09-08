from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth_deps import get_current_active_user
from app.services import image_verifier, rule_engine, decision_engine

router = APIRouter()

@router.post("/verify-packing")
async def verify_packing(
    part_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    image_data = await file.read()
    
    # Fetch Part
    part = db.query(models.Part).filter(models.Part.id == part_id).first()
    if not part:
        return {"status": "ERROR", "message": "Part not found"}
        
    part_requirements = {
        "required_box": part.required_box,
        "required_padding_mm": part.required_padding_mm,
        "required_orientation": part.required_orientation,
        "protective_cover_required": part.protective_cover_required,
        "min_image_quality": 0.80
    }
    
    # 1. Image verification
    features = image_verifier.verify_image(
        image_data, 
        metadata={"filename": file.filename, **part_requirements}
    )
    
    # 2. Rule evaluation
    rule_results = rule_engine.evaluate_rules(part_requirements, features)
    
    # 3. Decision making
    decision = decision_engine.make_decision(
        rule_results, 
        visual_confidence=features.get("confidence", 0.90), 
        image_quality=features.get("image_quality", 0.90)
    )
    
    # 4. Save result
    inspection = models.Inspection(
        part_id=part.part_id,
        operator_id=current_user.id,
        image_path=file.filename,
        decision=decision["decision"],
        confidence=features.get("confidence", 0.90),
        network_status="online",
        location_status="known",
        sensor_status="ok",
        manual_review_required=(decision["decision"] == "MANUAL_REVIEW")
    )
    db.add(inspection)
    db.commit()
    db.refresh(inspection)
    
    return {
        "status": decision["decision"], 
        "details": decision["explanation"], 
        "inspection_id": inspection.id,
        "rules": rule_results
    }

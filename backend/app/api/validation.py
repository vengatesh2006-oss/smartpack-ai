from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/")
def submit_validation_feedback(feedback: schemas.ValidationResponseCreate, db: Session = Depends(get_db)):
    new_feedback = models.ValidationResponse(**feedback.model_dump())
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

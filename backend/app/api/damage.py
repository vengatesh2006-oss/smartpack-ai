from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List

router = APIRouter()

@router.get("/")
def get_damage_outcomes(db: Session = Depends(get_db)):
    return db.query(models.DamageOutcome).all()

@router.post("/")
def create_damage_outcome(outcome: schemas.DamageOutcomeCreate, db: Session = Depends(get_db)):
    new_outcome = models.DamageOutcome(**outcome.model_dump())
    db.add(new_outcome)
    db.commit()
    db.refresh(new_outcome)
    return new_outcome

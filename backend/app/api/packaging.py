from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List

router = APIRouter()

@router.get("/{part_id}/rules")
def get_packaging_rules(part_id: int, db: Session = Depends(get_db)):
    rules = db.query(models.PackagingRule).filter(models.PackagingRule.part_id == part_id).all()
    return rules

import os
import sys
from datetime import datetime, timedelta
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from backend.app.database import engine, Base, SessionLocal
from backend.app.models import User, Part, PackagingRule, Inspection, DetectedError, DamageOutcome
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    if db.query(User).first():
        print("Database already seeded.")
        return

    dispatcher = User(username="dispatcher", name="Dispatcher", role="dispatcher", password_hash=get_password_hash("dispatcher123"))
    manager = User(username="manager", name="Manager", role="manager", password_hash=get_password_hash("manager123"))
    db.add(dispatcher)
    db.add(manager)
    
    parts = [
        Part(part_id="BRK-1025", part_name="Brake Pad Assembly", category="Brakes", weight=1.5, length=15.0, width=10.0, height=5.0, fragility="Low", surface_sensitivity="Medium", required_box="Standard", required_padding_mm=10.0, required_orientation="Upright", protective_cover_required=True, max_movement_mm=5.0),
        Part(part_id="ENG-2040", part_name="Engine Valve", category="Engine", weight=0.5, length=10.0, width=2.0, height=2.0, fragility="High", surface_sensitivity="High", required_box="Standard", required_padding_mm=20.0, required_orientation="Upright", protective_cover_required=True, max_movement_mm=2.0),
        Part(part_id="1", part_name="Test Part", category="Test", weight=0.5, length=10.0, width=2.0, height=2.0, fragility="High", surface_sensitivity="High", required_box="Standard", required_padding_mm=20.0, required_orientation="Upright", protective_cover_required=True, max_movement_mm=2.0)
    ]
    db.add_all(parts)
    db.commit()

    print("Database seeded successfully with real models.")

if __name__ == "__main__":
    seed_data()

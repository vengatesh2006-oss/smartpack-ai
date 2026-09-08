from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    name = Column(String)
    role = Column(String)
    active = Column(Boolean, default=True)


class Part(Base):
    __tablename__ = "parts"

    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(String, unique=True, index=True)
    part_name = Column(String)
    category = Column(String)
    weight = Column(Float)
    length = Column(Float)
    width = Column(Float)
    height = Column(Float)
    fragility = Column(String)
    surface_sensitivity = Column(String)
    required_box = Column(String)
    required_padding_mm = Column(Float)
    required_orientation = Column(String)
    protective_cover_required = Column(Boolean)
    max_movement_mm = Column(Float)
    active = Column(Boolean, default=True)


class PackagingRule(Base):
    __tablename__ = "packaging_rules"

    id = Column(Integer, primary_key=True, index=True)
    part_id = Column(String, index=True)
    rule_type = Column(String)
    rule_description = Column(Text)
    severity = Column(String)
    expected_value = Column(String)
    active = Column(Boolean, default=True)


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(String, index=True)
    part_id = Column(String, index=True)
    operator_id = Column(Integer, ForeignKey("users.id"))
    image_path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    decision = Column(String)
    confidence = Column(Float)
    network_status = Column(String)
    location_status = Column(String)
    sensor_status = Column(String)
    manual_review_required = Column(Boolean, default=False)
    manual_decision = Column(String, nullable=True)
    manual_reason = Column(Text, nullable=True)
    sync_status = Column(String, default="pending")


class DetectedError(Base):
    __tablename__ = "detected_errors"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"))
    error_type = Column(String)
    severity = Column(String)
    confidence = Column(Float)
    description = Column(Text)


class DamageOutcome(Base):
    __tablename__ = "damage_outcomes"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(String, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"))
    damage_found = Column(Boolean)
    damage_type = Column(String, nullable=True)
    damage_severity = Column(String, nullable=True)
    reported_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=True)
    action = Column(String)
    reason = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class ValidationResponse(Base):
    __tablename__ = "validation_responses"

    id = Column(Integer, primary_key=True, index=True)
    scenario = Column(String)
    ease_of_use = Column(Integer)
    clarity = Column(Integer)
    trust = Column(Integer)
    manual_intervention_score = Column(Integer)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

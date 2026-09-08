from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Login(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    username: str # Use email as username
    password: str
    role: str = "dispatcher"

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    name: str

class DashboardMetrics(BaseModel):
    total_inspections: int
    passed_inspections: int
    failed_inspections: int
    manual_reviews: int
    pending_syncs: int

class UserBase(BaseModel):
    username: str
    name: str
    role: str
    active: bool = True

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class PartBase(BaseModel):
    part_id: str
    part_name: str
    category: str
    weight: float
    length: float
    width: float
    height: float
    fragility: str
    surface_sensitivity: str
    required_box: str
    required_padding_mm: float
    required_orientation: str
    protective_cover_required: bool
    max_movement_mm: float
    active: bool = True

class PartCreate(PartBase):
    pass

class PartResponse(PartBase):
    id: int

    class Config:
        from_attributes = True

class PackagingRuleBase(BaseModel):
    part_id: str
    rule_type: str
    rule_description: str
    severity: str
    expected_value: str
    active: bool = True

class PackagingRuleCreate(PackagingRuleBase):
    pass

class PackagingRuleResponse(PackagingRuleBase):
    id: int

    class Config:
        from_attributes = True

class InspectionBase(BaseModel):
    shipment_id: str
    part_id: str
    operator_id: int
    image_path: str
    decision: str
    confidence: float
    network_status: str
    location_status: str
    sensor_status: str
    manual_review_required: bool = False
    manual_decision: Optional[str] = None
    manual_reason: Optional[str] = None
    sync_status: str = "pending"

class InspectionCreate(InspectionBase):
    pass

class InspectionResponse(InspectionBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class DetectedErrorBase(BaseModel):
    inspection_id: int
    error_type: str
    severity: str
    confidence: float
    description: str

class DetectedErrorCreate(DetectedErrorBase):
    pass

class DetectedErrorResponse(DetectedErrorBase):
    id: int

    class Config:
        from_attributes = True

class DamageOutcomeBase(BaseModel):
    shipment_id: str
    inspection_id: int
    damage_found: bool
    damage_type: Optional[str] = None
    damage_severity: Optional[str] = None
    notes: Optional[str] = None

class DamageOutcomeCreate(DamageOutcomeBase):
    pass

class DamageOutcomeResponse(DamageOutcomeBase):
    id: int
    reported_date: datetime

    class Config:
        from_attributes = True

class AuditLogBase(BaseModel):
    user_id: int
    inspection_id: Optional[int] = None
    action: str
    reason: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogResponse(AuditLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class ValidationResponseBase(BaseModel):
    scenario: str
    ease_of_use: int
    clarity: int
    trust: int
    manual_intervention_score: int
    comments: Optional[str] = None

class ValidationResponseCreate(ValidationResponseBase):
    pass

class ValidationResponseResponse(ValidationResponseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SyncRequest(BaseModel):
    inspections: List[InspectionCreate]
    audit_logs: List[AuditLogCreate]
    detected_errors: List[DetectedErrorCreate]

class ManualDecision(BaseModel):
    decision: str
    reason: str

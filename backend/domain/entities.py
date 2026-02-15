from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    GERENTE = "gerente"
    SUPERVISOR = "supervisor"
    JURIDICO = "juridico"
    RH = "rh"

class MeasureType(str, Enum):
    ADVERTENCIA = "advertencia"
    SUSPENSAO = "suspensao"

class MeasureStatus(str, Enum):
    PENDENTE = "pendente"
    ASSINADO = "assinado"
    CANCELADO = "cancelado"

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    name: str
    email: EmailStr
    role: UserRole
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Employee(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    name: str
    cpf: str
    department: str
    position: str
    admission_date: datetime
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Measure(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    employee_id: str
    employee_name: str
    measure_type: MeasureType
    reason: str
    description: str
    applied_by_id: str
    applied_by_name: str
    status: MeasureStatus
    suspension_days: Optional[int] = None
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    signed_at: Optional[datetime] = None
    signed_by_id: Optional[str] = None
    signed_by_name: Optional[str] = None
    canceled_at: Optional[datetime] = None
    canceled_by_id: Optional[str] = None
    canceled_reason: Optional[str] = None

class AuditLog(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    action: str
    entity_type: str
    entity_id: str
    user_id: str
    user_name: str
    user_role: UserRole
    details: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)

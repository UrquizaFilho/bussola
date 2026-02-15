from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from domain.entities import UserRole, MeasureType, MeasureStatus

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str
    user: dict

class CreateEmployeeRequest(BaseModel):
    name: str
    cpf: str
    department: str
    position: str
    admission_date: datetime

class UpdateEmployeeRequest(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    active: Optional[bool] = None

class CreateMeasureRequest(BaseModel):
    employee_id: str
    measure_type: MeasureType
    reason: str
    description: str
    suspension_days: Optional[int] = None

class SignMeasureRequest(BaseModel):
    measure_id: str

class CancelMeasureRequest(BaseModel):
    measure_id: str
    reason: str

class DashboardStatsResponse(BaseModel):
    total_measures_month: int
    pending_measures: int
    total_employees: int
    measures_by_type: dict

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from domain.entities import UserRole, MeasureType, MeasureStatus, InfractionCategory

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str
    user: dict

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole
    manager_id: Optional[str] = None
    team_id: Optional[str] = None

class CreateEmployeeRequest(BaseModel):
    name: str
    cpf: str
    email: EmailStr
    department: str
    position: str
    admission_date: datetime
    supervisor_id: Optional[str] = None
    team_id: Optional[str] = None

class UpdateEmployeeRequest(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    supervisor_id: Optional[str] = None
    team_id: Optional[str] = None
    active: Optional[bool] = None

class CreateMeasureRequest(BaseModel):
    employee_id: str
    measure_type: MeasureType
    infraction_category: InfractionCategory
    reason: str
    description: str
    suspension_days: Optional[int] = None

class AcknowledgeMeasureRequest(BaseModel):
    measure_id: str

class AcknowledgeWithWitnessesRequest(BaseModel):
    measure_id: str
    witness1_email: EmailStr
    witness1_password: str
    witness2_email: EmailStr
    witness2_password: str

class SignMeasureRequest(BaseModel):
    measure_id: str

class CancelMeasureRequest(BaseModel):
    measure_id: str
    reason: str

class CreateTeamRequest(BaseModel):
    name: str
    manager_id: str
    parent_team_id: Optional[str] = None
    level: str

class MigrateEmployeeRequest(BaseModel):
    employee_id: str
    new_supervisor_id: str
    new_team_id: str

class DashboardStatsResponse(BaseModel):
    total_measures_month: int
    pending_measures: int
    total_employees: int
    measures_by_type: dict
    my_team_size: int

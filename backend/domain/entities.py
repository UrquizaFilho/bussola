from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    GERENTE = "gerente"
    COORDENADOR = "coordenador"
    SUPERVISOR = "supervisor"
    COLABORADOR = "colaborador"
    JURIDICO = "juridico"
    RH = "rh"

class MeasureType(str, Enum):
    ADVERTENCIA_VERBAL = "advertencia_verbal"
    ADVERTENCIA_ESCRITA = "advertencia_escrita"
    SUSPENSAO = "suspensao"

class MeasureStatus(str, Enum):
    PENDENTE_RECEBIMENTO = "pendente_recebimento"
    RECEBIDO = "recebido"
    RECEBIDO_COM_TESTEMUNHAS = "recebido_com_testemunhas"
    ASSINADO = "assinado"
    CANCELADO = "cancelado"

class InfractionCategory(str, Enum):
    ATRASO = "atraso"
    FALTA_INJUSTIFICADA = "falta_injustificada"
    DESCUMPRIMENTO_NORMAS = "descumprimento_normas"
    INSUBORDINACAO = "insubordinacao"
    DESRESPEITO = "desrespeito"
    NEGLIGENCIA = "negligencia"
    USO_INDEVIDO_RECURSOS = "uso_indevido_recursos"
    OUTROS = "outros"

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    name: str
    email: EmailStr
    role: UserRole
    manager_id: Optional[str] = None
    team_id: Optional[str] = None
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Employee(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    name: str
    cpf: str
    email: EmailStr
    department: str
    position: str
    admission_date: datetime
    supervisor_id: Optional[str] = None
    team_id: Optional[str] = None
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Team(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    name: str
    manager_id: str
    manager_name: str
    parent_team_id: Optional[str] = None
    level: str  # gerente, coordenador, supervisor
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Witness(BaseModel):
    user_id: str
    user_name: str
    user_role: UserRole
    timestamp: datetime

class Measure(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    employee_id: str
    employee_name: str
    measure_type: MeasureType
    infraction_category: InfractionCategory
    reason: str
    description: str
    applied_by_id: str
    applied_by_name: str
    status: MeasureStatus
    suspension_days: Optional[int] = None
    document_template_path: Optional[str] = None
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Recebimento
    acknowledged_at: Optional[datetime] = None
    acknowledged_by_id: Optional[str] = None
    acknowledged_by_name: Optional[str] = None
    witnesses: Optional[List[Witness]] = None
    
    # Assinatura (RH/Jurídico)
    signed_at: Optional[datetime] = None
    signed_by_id: Optional[str] = None
    signed_by_name: Optional[str] = None
    
    # Cancelamento
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

class DocumentTemplate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str
    name: str
    measure_type: MeasureType
    file_path: str
    uploaded_by_id: str
    uploaded_by_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

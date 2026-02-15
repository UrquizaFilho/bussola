from infrastructure.repositories import (
    UserRepository, EmployeeRepository, MeasureRepository, 
    AuditLogRepository, TeamRepository, DocumentTemplateRepository
)
from infrastructure.auth import verify_password, get_password_hash, create_access_token
from domain.entities import (
    User, Employee, Measure, AuditLog, Team, Witness,
    UserRole, MeasureStatus, MeasureType, InfractionCategory
)
from application.dto import (
    CreateEmployeeRequest, CreateMeasureRequest, DashboardStatsResponse,
    CreateUserRequest, CreateTeamRequest, MigrateEmployeeRequest
)
from application.measure_validation import MeasureEscalationValidator
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import uuid

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def login(self, email: str, password: str) -> Optional[dict]:
        user_doc = await self.user_repo.find_by_email(email)
        if not user_doc:
            return None
        
        if not verify_password(password, user_doc['password_hash']):
            return None
        
        if not user_doc.get('active', True):
            return None
        
        token = create_access_token(data={"sub": user_doc['id'], "email": email, "role": user_doc['role']})
        
        user_data = {k: v for k, v in user_doc.items() if k != 'password_hash'}
        return {"token": token, "user": user_data}
    
    async def create_user(self, name: str, email: str, password: str, role: UserRole) -> User:
        existing = await self.user_repo.find_by_email(email)
        if existing:
            raise ValueError("Email já cadastrado")
        
        user_id = str(uuid.uuid4())
        user_doc = {
            "id": user_id,
            "name": name,
            "email": email,
            "password_hash": get_password_hash(password),
            "role": role.value,
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await self.user_repo.create(user_doc)
        return User(**{k: v for k, v in user_doc.items() if k != 'password_hash'})

class EmployeeService:
    def __init__(self, employee_repo: EmployeeRepository, audit_repo: AuditLogRepository):
        self.employee_repo = employee_repo
        self.audit_repo = audit_repo
    
    async def create_employee(self, request: CreateEmployeeRequest, user: dict) -> Employee:
        existing = await self.employee_repo.find_by_cpf(request.cpf)
        if existing:
            raise ValueError("CPF já cadastrado")
        
        employee_id = str(uuid.uuid4())
        employee_doc = {
            "id": employee_id,
            "name": request.name,
            "cpf": request.cpf,
            "department": request.department,
            "position": request.position,
            "admission_date": request.admission_date.isoformat(),
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await self.employee_repo.create(employee_doc)
        
        await self._create_audit_log("CREATE_EMPLOYEE", "employee", employee_id, user, {"employee_name": request.name})
        
        return Employee(**employee_doc)
    
    async def get_employees(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        docs = await self.employee_repo.find_all({"active": True}, skip, limit)
        return [Employee(**doc) for doc in docs]
    
    async def get_employee_by_id(self, employee_id: str) -> Optional[Employee]:
        doc = await self.employee_repo.find_by_id(employee_id)
        return Employee(**doc) if doc else None
    
    async def update_employee(self, employee_id: str, update_data: dict, user: dict) -> Optional[Employee]:
        doc = await self.employee_repo.update(employee_id, update_data)
        if doc:
            await self._create_audit_log("UPDATE_EMPLOYEE", "employee", employee_id, user, update_data)
        return Employee(**doc) if doc else None
    
    async def _create_audit_log(self, action: str, entity_type: str, entity_id: str, user: dict, details: dict):
        log_doc = {
            "id": str(uuid.uuid4()),
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "user_id": user['id'],
            "user_name": user['name'],
            "user_role": user['role'],
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await self.audit_repo.create(log_doc)

class MeasureService:
    def __init__(self, measure_repo: MeasureRepository, employee_repo: EmployeeRepository, audit_repo: AuditLogRepository):
        self.measure_repo = measure_repo
        self.employee_repo = employee_repo
        self.audit_repo = audit_repo
    
    async def create_measure(self, request: CreateMeasureRequest, user: dict) -> Measure:
        employee = await self.employee_repo.find_by_id(request.employee_id)
        if not employee:
            raise ValueError("Colaborador não encontrado")
        
        if not employee.get('active', True):
            raise ValueError("Colaborador inativo")
        
        # VALIDAÇÃO: Verificar escalonamento de medidas
        previous_measures = await self.measure_repo.find_by_employee(request.employee_id)
        
        is_valid, error_msg = MeasureEscalationValidator.validate_measure_escalation(
            previous_measures,
            request.infraction_category,
            request.measure_type
        )
        
        if not is_valid:
            raise ValueError(error_msg)
        
        measure_id = str(uuid.uuid4())
        measure_doc = {
            "id": measure_id,
            "employee_id": request.employee_id,
            "employee_name": employee['name'],
            "measure_type": request.measure_type.value,
            "infraction_category": request.infraction_category.value,
            "reason": request.reason,
            "description": request.description,
            "applied_by_id": user['id'],
            "applied_by_name": user['name'],
            "status": MeasureStatus.PENDENTE_RECEBIMENTO.value,
            "suspension_days": request.suspension_days,
            "applied_at": datetime.now(timezone.utc).isoformat(),
            "acknowledged_at": None,
            "acknowledged_by_id": None,
            "acknowledged_by_name": None,
            "witnesses": None,
            "signed_at": None,
            "signed_by_id": None,
            "signed_by_name": None,
            "canceled_at": None,
            "canceled_by_id": None,
            "canceled_reason": None,
            "document_template_path": None
        }
        
        await self.measure_repo.create(measure_doc)
        
        await self._create_audit_log("APPLY_MEASURE", "measure", measure_id, user, {
            "employee_name": employee['name'],
            "measure_type": request.measure_type.value,
            "infraction_category": request.infraction_category.value
        })
        
        return Measure(**measure_doc)
        
        await self._create_audit_log("APPLY_MEASURE", "measure", measure_id, user, {
            "employee_name": employee['name'],
            "measure_type": request.measure_type.value
        })
        
        return Measure(**measure_doc)
    
    async def sign_measure(self, measure_id: str, user: dict) -> Optional[Measure]:
        if user['role'] not in [UserRole.JURIDICO.value, UserRole.RH.value]:
            raise ValueError("Apenas Jurídico ou RH podem assinar medidas")
        
        measure = await self.measure_repo.find_by_id(measure_id)
        if not measure:
            raise ValueError("Medida não encontrada")
        
        if measure['status'] not in [MeasureStatus.PENDENTE_RECEBIMENTO.value, MeasureStatus.RECEBIDO.value, MeasureStatus.RECEBIDO_COM_TESTEMUNHAS.value]:
            raise ValueError("Apenas medidas recebidas podem ser assinadas")
        
        update_data = {
            "status": MeasureStatus.ASSINADO.value,
            "signed_at": datetime.now(timezone.utc).isoformat(),
            "signed_by_id": user['id'],
            "signed_by_name": user['name']
        }
        
        doc = await self.measure_repo.update(measure_id, update_data)
        
        await self._create_audit_log("SIGN_MEASURE", "measure", measure_id, user, {"employee_name": measure['employee_name']})
        
        return Measure(**doc) if doc else None
    
    async def cancel_measure(self, measure_id: str, reason: str, user: dict) -> Optional[Measure]:
        if user['role'] not in [UserRole.JURIDICO.value, UserRole.RH.value]:
            raise ValueError("Apenas Jurídico ou RH podem cancelar medidas")
        
        measure = await self.measure_repo.find_by_id(measure_id)
        if not measure:
            raise ValueError("Medida não encontrada")
        
        update_data = {
            "status": MeasureStatus.CANCELADO.value,
            "canceled_at": datetime.now(timezone.utc).isoformat(),
            "canceled_by_id": user['id'],
            "canceled_reason": reason
        }
        
        doc = await self.measure_repo.update(measure_id, update_data)
        
        await self._create_audit_log("CANCEL_MEASURE", "measure", measure_id, user, {"reason": reason})
        
        return Measure(**doc) if doc else None
    
    async def get_measures(self, skip: int = 0, limit: int = 100) -> List[Measure]:
        docs = await self.measure_repo.find_all({}, skip, limit)
        return [Measure(**doc) for doc in docs]
    
    async def get_employee_measures(self, employee_id: str) -> List[Measure]:
        docs = await self.measure_repo.find_by_employee(employee_id)
        return [Measure(**doc) for doc in docs]
    
    async def get_dashboard_stats(self) -> DashboardStatsResponse:
        now = datetime.now(timezone.utc)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        all_measures = await self.measure_repo.find_all({})
        month_measures = [m for m in all_measures if datetime.fromisoformat(m['applied_at']) >= month_start]
        pending = [m for m in all_measures if m['status'] == MeasureStatus.PENDENTE_RECEBIMENTO.value]
        
        measures_by_type = {
            "advertencia_verbal": len([m for m in month_measures if m['measure_type'] == MeasureType.ADVERTENCIA_VERBAL.value]),
            "advertencia_escrita": len([m for m in month_measures if m['measure_type'] == MeasureType.ADVERTENCIA_ESCRITA.value]),
            "suspensao": len([m for m in month_measures if m['measure_type'] == MeasureType.SUSPENSAO.value])
        }
        
        total_employees = await self.employee_repo.count({"active": True})
        
        return DashboardStatsResponse(
            total_measures_month=len(month_measures),
            pending_measures=len(pending),
            total_employees=total_employees,
            measures_by_type=measures_by_type
        )
    
    async def _create_audit_log(self, action: str, entity_type: str, entity_id: str, user: dict, details: dict):
        log_doc = {
            "id": str(uuid.uuid4()),
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "user_id": user['id'],
            "user_name": user['name'],
            "user_role": user['role'],
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await self.audit_repo.create(log_doc)

class AuditService:
    def __init__(self, audit_repo: AuditLogRepository):
        self.audit_repo = audit_repo
    
    async def get_recent_logs(self, limit: int = 100) -> List[AuditLog]:
        docs = await self.audit_repo.find_recent(limit)
        return [AuditLog(**doc) for doc in docs]

    async def acknowledge_measure(self, measure_id: str, user: dict) -> Optional[Measure]:
        """Colaborador dá RECEBIDO na medida"""
        measure = await self.measure_repo.find_by_id(measure_id)
        if not measure:
            raise ValueError("Medida não encontrada")
        
        if measure['status'] != MeasureStatus.PENDENTE_RECEBIMENTO.value:
            raise ValueError("Medida não está pendente de recebimento")
        
        # Verificar se é o próprio colaborador
        employee = await self.employee_repo.find_by_id(measure['employee_id'])
        if not employee or employee.get('email') != user.get('email'):
            raise ValueError("Apenas o colaborador pode dar recebido na própria medida")
        
        update_data = {
            "status": MeasureStatus.RECEBIDO.value,
            "acknowledged_at": datetime.now(timezone.utc).isoformat(),
            "acknowledged_by_id": user['id'],
            "acknowledged_by_name": user['name']
        }
        
        doc = await self.measure_repo.update(measure_id, update_data)
        
        await self._create_audit_log("ACKNOWLEDGE_MEASURE", "measure", measure_id, user, {
            "employee_name": measure['employee_name']
        })
        
        return Measure(**doc) if doc else None
    
    async def acknowledge_with_witnesses(
        self, 
        measure_id: str, 
        witness1_email: str, 
        witness1_password: str,
        witness2_email: str,
        witness2_password: str,
        supervisor: dict,
        user_repo
    ) -> Optional[Measure]:
        """Supervisor dá RECEBIDO com 2 testemunhas quando colaborador se recusa"""
        measure = await self.measure_repo.find_by_id(measure_id)
        if not measure:
            raise ValueError("Medida não encontrada")
        
        if measure['status'] != MeasureStatus.PENDENTE_RECEBIMENTO.value:
            raise ValueError("Medida não está pendente de recebimento")
        
        # Validar testemunha 1
        witness1 = await user_repo.find_by_email(witness1_email)
        if not witness1:
            raise ValueError("Primeira testemunha não encontrada")
        
        if not verify_password(witness1_password, witness1['password_hash']):
            raise ValueError("Senha incorreta para primeira testemunha")
        
        if witness1['role'] not in [UserRole.GERENTE.value, UserRole.COORDENADOR.value, UserRole.SUPERVISOR.value]:
            raise ValueError("Primeira testemunha deve ser Gerente, Coordenador ou Supervisor")
        
        # Validar testemunha 2
        witness2 = await user_repo.find_by_email(witness2_email)
        if not witness2:
            raise ValueError("Segunda testemunha não encontrada")
        
        if not verify_password(witness2_password, witness2['password_hash']):
            raise ValueError("Senha incorreta para segunda testemunha")
        
        if witness2['role'] not in [UserRole.GERENTE.value, UserRole.COORDENADOR.value, UserRole.SUPERVISOR.value]:
            raise ValueError("Segunda testemunha deve ser Gerente, Coordenador ou Supervisor")
        
        # Testemunhas não podem ser a mesma pessoa
        if witness1['id'] == witness2['id']:
            raise ValueError("As testemunhas devem ser pessoas diferentes")
        
        now = datetime.now(timezone.utc).isoformat()
        witnesses_data = [
            {
                "user_id": witness1['id'],
                "user_name": witness1['name'],
                "user_role": witness1['role'],
                "timestamp": now
            },
            {
                "user_id": witness2['id'],
                "user_name": witness2['name'],
                "user_role": witness2['role'],
                "timestamp": now
            }
        ]
        
        update_data = {
            "status": MeasureStatus.RECEBIDO_COM_TESTEMUNHAS.value,
            "acknowledged_at": now,
            "acknowledged_by_id": supervisor['id'],
            "acknowledged_by_name": supervisor['name'],
            "witnesses": witnesses_data
        }
        
        doc = await self.measure_repo.update(measure_id, update_data)
        
        await self._create_audit_log("ACKNOWLEDGE_WITH_WITNESSES", "measure", measure_id, supervisor, {
            "employee_name": measure['employee_name'],
            "witnesses": [witness1['name'], witness2['name']]
        })
        
        return Measure(**doc) if doc else None

class TeamService:
    def __init__(self, team_repo: TeamRepository, user_repo: UserRepository, employee_repo: EmployeeRepository, audit_repo: AuditLogRepository):
        self.team_repo = team_repo
        self.user_repo = user_repo
        self.employee_repo = employee_repo
        self.audit_repo = audit_repo
    
    async def create_team(self, request: CreateTeamRequest, user: dict) -> Team:
        manager = await self.user_repo.find_by_id(request.manager_id)
        if not manager:
            raise ValueError("Gerente não encontrado")
        
        team_id = str(uuid.uuid4())
        team_doc = {
            "id": team_id,
            "name": request.name,
            "manager_id": request.manager_id,
            "manager_name": manager['name'],
            "parent_team_id": request.parent_team_id,
            "level": request.level,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        await self.team_repo.create(team_doc)
        
        await self._create_audit_log("CREATE_TEAM", "team", team_id, user, {
            "team_name": request.name,
            "manager": manager['name']
        })
        
        return Team(**team_doc)
    
    async def migrate_employee(self, request: MigrateEmployeeRequest, user: dict) -> Optional[Employee]:
        """Migra colaborador para nova equipe/supervisor"""
        employee = await self.employee_repo.find_by_id(request.employee_id)
        if not employee:
            raise ValueError("Colaborador não encontrado")
        
        new_supervisor = await self.user_repo.find_by_id(request.new_supervisor_id)
        if not new_supervisor:
            raise ValueError("Novo supervisor não encontrado")
        
        update_data = {
            "supervisor_id": request.new_supervisor_id,
            "team_id": request.new_team_id
        }
        
        doc = await self.employee_repo.update(request.employee_id, update_data)
        
        await self._create_audit_log("MIGRATE_EMPLOYEE", "employee", request.employee_id, user, {
            "employee_name": employee['name'],
            "new_supervisor": new_supervisor['name']
        })
        
        return Employee(**doc) if doc else None
    
    async def get_team_hierarchy(self, user: dict) -> dict:
        """Retorna hierarquia de equipes do usuário"""
        teams = await self.team_repo.find_by_manager(user['id'])
        
        hierarchy = {
            "direct_reports": [],
            "teams": teams
        }
        
        # Buscar subordinados diretos
        if user['role'] in [UserRole.GERENTE.value, UserRole.COORDENADOR.value, UserRole.SUPERVISOR.value]:
            direct_reports = await self.user_repo.find_by_manager(user['id'])
            hierarchy["direct_reports"] = direct_reports
        
        return hierarchy
    
    async def _create_audit_log(self, action: str, entity_type: str, entity_id: str, user: dict, details: dict):
        log_doc = {
            "id": str(uuid.uuid4()),
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "user_id": user['id'],
            "user_name": user['name'],
            "user_role": user['role'],
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await self.audit_repo.create(log_doc)


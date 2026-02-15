from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File
from fastapi.responses import FileResponse
from application.dto import (
    LoginRequest, LoginResponse,
    CreateEmployeeRequest, UpdateEmployeeRequest,
    CreateMeasureRequest, AcknowledgeMeasureRequest, AcknowledgeWithWitnessesRequest,
    SignMeasureRequest, CancelMeasureRequest,
    CreateTeamRequest, MigrateEmployeeRequest, CreateUserRequest,
    DashboardStatsResponse
)
from application.services import AuthService, EmployeeService, MeasureService, AuditService, TeamService
from infrastructure.repositories import (
    UserRepository, EmployeeRepository, MeasureRepository, 
    AuditLogRepository, TeamRepository, DocumentTemplateRepository
)
from interfaces.middleware import get_current_user, require_roles
import os
import shutil
from pathlib import Path

auth_router = APIRouter()
employee_router = APIRouter()
measure_router = APIRouter()
audit_router = APIRouter()
team_router = APIRouter()
document_router = APIRouter()
user_router = APIRouter()

UPLOAD_DIR = Path("/app/backend/uploads/templates")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def get_db(request: Request):
    return request.app.state.db

# ============= AUTH ROUTES =============

@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    
    result = await auth_service.login(request.email, request.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    return result

@auth_router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    user_repo = UserRepository(db)
    user_doc = await user_repo.find_by_id(current_user['sub'])
    if not user_doc:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {k: v for k, v in user_doc.items() if k != 'password_hash'}

# ============= USER ROUTES =============

@user_router.post("/")
async def create_user(request: CreateUserRequest, current_user: dict = Depends(require_roles(["rh"])), db = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    
    try:
        user = await auth_service.create_user(
            request.name,
            request.email,
            request.password,
            request.role
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_router.get("/")
async def get_users(current_user: dict = Depends(require_roles(["rh", "gerente"])), db = Depends(get_db)):
    user_repo = UserRepository(db)
    users = await user_repo.find_all({"active": True})
    return [{k: v for k, v in u.items() if k != 'password_hash'} for u in users]

@user_router.get("/hierarchy")
async def get_my_hierarchy(current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    team_repo = TeamRepository(db)
    user_repo = UserRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    
    team_service = TeamService(team_repo, user_repo, employee_repo, audit_repo)
    
    user_doc = await user_repo.find_by_id(current_user['sub'])
    hierarchy = await team_service.get_team_hierarchy(user_doc)
    
    return hierarchy

# ============= EMPLOYEE ROUTES =============

@employee_router.post("/")
async def create_employee(request: CreateEmployeeRequest, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    employee_service = EmployeeService(employee_repo, audit_repo)
    
    user_repo = UserRepository(db)
    user_doc = await user_repo.find_by_id(current_user['sub'])
    
    try:
        employee = await employee_service.create_employee(request, user_doc)
        return employee
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@employee_router.get("/")
async def get_employees(skip: int = 0, limit: int = 100, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    employee_service = EmployeeService(employee_repo, audit_repo)
    
    employees = await employee_service.get_employees(skip, limit)
    return employees

@employee_router.get("/my-team")
async def get_my_team_employees(current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    user_repo = UserRepository(db)
    employee_repo = EmployeeRepository(db)
    
    user_doc = await user_repo.find_by_id(current_user['sub'])
    
    # Buscar colaboradores supervisionados
    if user_doc.get('role') in ['supervisor', 'coordenador', 'gerente']:
        employees = await employee_repo.find_by_supervisor(user_doc['id'])
        return employees
    
    return []

@employee_router.get("/{employee_id}")
async def get_employee(employee_id: str, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    employee_service = EmployeeService(employee_repo, audit_repo)
    
    employee = await employee_service.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return employee

@employee_router.patch("/{employee_id}")
async def update_employee(employee_id: str, request: UpdateEmployeeRequest, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    employee_service = EmployeeService(employee_repo, audit_repo)
    
    user_repo = UserRepository(db)
    user_doc = await user_repo.find_by_id(current_user['sub'])
    
    update_data = {k: v for k, v in request.model_dump().items() if v is not None}
    employee = await employee_service.update_employee(employee_id, update_data, user_doc)
    
    if not employee:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return employee

# ============= MEASURE ROUTES =============

@measure_router.post("/")
async def create_measure(request: CreateMeasureRequest, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    measure_repo = MeasureRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    measure_service = MeasureService(measure_repo, employee_repo, audit_repo)
    
    user_repo = UserRepository(db)
    user_doc = await user_repo.find_by_id(current_user['sub'])
    
    try:
        measure = await measure_service.create_measure(request, user_doc)
        return measure
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@measure_router.get("/")
async def get_measures(skip: int = 0, limit: int = 100, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    measure_repo = MeasureRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    measure_service = MeasureService(measure_repo, employee_repo, audit_repo)
    
    measures = await measure_service.get_measures(skip, limit)
    return measures

@measure_router.get("/dashboard/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    measure_repo = MeasureRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    measure_service = MeasureService(measure_repo, employee_repo, audit_repo)
    
    stats = await measure_service.get_dashboard_stats()
    return stats

@measure_router.get("/employee/{employee_id}")
async def get_employee_measures(employee_id: str, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    measure_repo = MeasureRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    measure_service = MeasureService(measure_repo, employee_repo, audit_repo)
    
    measures = await measure_service.get_employee_measures(employee_id)
    return measures

@measure_router.post("/acknowledge")
async def acknowledge_measure(request: AcknowledgeMeasureRequest, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    """Colaborador dá RECEBIDO na medida"""
    measure_repo = MeasureRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    measure_service = MeasureService(measure_repo, employee_repo, audit_repo)
    
    user_repo = UserRepository(db)
    user_doc = await user_repo.find_by_id(current_user['sub'])
    
    try:
        measure = await measure_service.acknowledge_measure(request.measure_id, user_doc)
        if not measure:
            raise HTTPException(status_code=404, detail="Medida não encontrada")
        return measure
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@measure_router.post("/acknowledge-witnesses")
async def acknowledge_with_witnesses(
    request: AcknowledgeWithWitnessesRequest, 
    current_user: dict = Depends(require_roles(["supervisor", "coordenador", "gerente"])), 
    db = Depends(get_db)
):
    """Supervisor dá RECEBIDO com 2 testemunhas quando colaborador recusa"""
    measure_repo = MeasureRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    user_repo = UserRepository(db)
    
    measure_service = MeasureService(measure_repo, employee_repo, audit_repo)
    
    supervisor_doc = await user_repo.find_by_id(current_user['sub'])
    
    try:
        measure = await measure_service.acknowledge_with_witnesses(
            request.measure_id,
            request.witness1_email,
            request.witness1_password,
            request.witness2_email,
            request.witness2_password,
            supervisor_doc,
            user_repo
        )
        if not measure:
            raise HTTPException(status_code=404, detail="Medida não encontrada")
        return measure
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@measure_router.post("/sign")
async def sign_measure(request: SignMeasureRequest, current_user: dict = Depends(require_roles(["juridico", "rh"])), db = Depends(get_db)):
    measure_repo = MeasureRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    measure_service = MeasureService(measure_repo, employee_repo, audit_repo)
    
    user_repo = UserRepository(db)
    user_doc = await user_repo.find_by_id(current_user['sub'])
    
    try:
        measure = await measure_service.sign_measure(request.measure_id, user_doc)
        if not measure:
            raise HTTPException(status_code=404, detail="Medida não encontrada")
        return measure
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@measure_router.post("/cancel")
async def cancel_measure(request: CancelMeasureRequest, current_user: dict = Depends(require_roles(["juridico", "rh"])), db = Depends(get_db)):
    measure_repo = MeasureRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    measure_service = MeasureService(measure_repo, employee_repo, audit_repo)
    
    user_repo = UserRepository(db)
    user_doc = await user_repo.find_by_id(current_user['sub'])
    
    try:
        measure = await measure_service.cancel_measure(request.measure_id, request.reason, user_doc)
        if not measure:
            raise HTTPException(status_code=404, detail="Medida não encontrada")
        return measure
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============= TEAM ROUTES =============

@team_router.post("/")
async def create_team(request: CreateTeamRequest, current_user: dict = Depends(require_roles(["rh", "gerente"])), db = Depends(get_db)):
    team_repo = TeamRepository(db)
    user_repo = UserRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    
    team_service = TeamService(team_repo, user_repo, employee_repo, audit_repo)
    
    user_doc = await user_repo.find_by_id(current_user['sub'])
    
    try:
        team = await team_service.create_team(request, user_doc)
        return team
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@team_router.get("/")
async def get_teams(current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    team_repo = TeamRepository(db)
    teams = await team_repo.find_all()
    return teams

@team_router.post("/migrate-employee")
async def migrate_employee(
    request: MigrateEmployeeRequest, 
    current_user: dict = Depends(require_roles(["gerente", "coordenador", "supervisor"])), 
    db = Depends(get_db)
):
    team_repo = TeamRepository(db)
    user_repo = UserRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    
    team_service = TeamService(team_repo, user_repo, employee_repo, audit_repo)
    
    user_doc = await user_repo.find_by_id(current_user['sub'])
    
    try:
        employee = await team_service.migrate_employee(request, user_doc)
        if not employee:
            raise HTTPException(status_code=404, detail="Colaborador não encontrado")
        return employee
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============= DOCUMENT ROUTES =============

@document_router.post("/templates/upload")
async def upload_template(
    file: UploadFile = File(...),
    measure_type: str = None,
    current_user: dict = Depends(require_roles(["rh"])),
    db = Depends(get_db)
):
    """Upload de template Word para medidas"""
    if not file.filename.endswith(('.doc', '.docx')):
        raise HTTPException(status_code=400, detail="Apenas arquivos Word são permitidos")
    
    # Salvar arquivo
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Registrar no banco
    template_repo = DocumentTemplateRepository(db)
    user_repo = UserRepository(db)
    user_doc = await user_repo.find_by_id(current_user['sub'])
    
    template_doc = {
        "id": str(uuid.uuid4()),
        "name": file.filename,
        "measure_type": measure_type,
        "file_path": str(file_path),
        "uploaded_by_id": user_doc['id'],
        "uploaded_by_name": user_doc['name'],
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await template_repo.create(template_doc)
    
    return {"message": "Template enviado com sucesso", "template_id": template_doc['id']}

@document_router.get("/templates")
async def get_templates(current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    """Listar templates disponíveis"""
    template_repo = DocumentTemplateRepository(db)
    templates = await template_repo.find_all()
    return templates

@document_router.get("/templates/download/{template_id}")
async def download_template(template_id: str, current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    """Download de template"""
    template_repo = DocumentTemplateRepository(db)
    template = await template_repo.find_by_id(template_id)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    
    file_path = Path(template['file_path'])
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    return FileResponse(
        path=file_path,
        filename=template['name'],
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

# ============= AUDIT ROUTES =============

@audit_router.get("/logs")
async def get_audit_logs(limit: int = 100, current_user: dict = Depends(require_roles(["juridico", "rh"])), db = Depends(get_db)):
    audit_repo = AuditLogRepository(db)
    audit_service = AuditService(audit_repo)
    
    logs = await audit_service.get_recent_logs(limit)
    return logs

from fastapi import APIRouter, Depends, HTTPException, status, Request
from application.dto import (
    LoginRequest, LoginResponse,
    CreateEmployeeRequest, UpdateEmployeeRequest,
    CreateMeasureRequest, SignMeasureRequest, CancelMeasureRequest,
    DashboardStatsResponse
)
from application.services import AuthService, EmployeeService, MeasureService, AuditService
from infrastructure.repositories import UserRepository, EmployeeRepository, MeasureRepository, AuditLogRepository
from interfaces.middleware import get_current_user, require_roles

auth_router = APIRouter()
employee_router = APIRouter()
measure_router = APIRouter()
audit_router = APIRouter()

def get_db(request: Request):
    return request.app.state.db

@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
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
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    user_repo = UserRepository(db)
    user_doc = await user_repo.find_by_id(current_user['sub'])
    if not user_doc:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {k: v for k, v in user_doc.items() if k != 'password_hash'}

@employee_router.post("/")
async def create_employee(request: CreateEmployeeRequest, current_user: dict = Depends(get_current_user)):
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
async def get_employees(skip: int = 0, limit: int = 100, current_user: dict = Depends(get_current_user)):
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    employee_service = EmployeeService(employee_repo, audit_repo)
    
    employees = await employee_service.get_employees(skip, limit)
    return employees

@employee_router.get("/{employee_id}")
async def get_employee(employee_id: str, current_user: dict = Depends(get_current_user)):
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    employee_service = EmployeeService(employee_repo, audit_repo)
    
    employee = await employee_service.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    return employee

@employee_router.patch("/{employee_id}")
async def update_employee(employee_id: str, request: UpdateEmployeeRequest, current_user: dict = Depends(get_current_user)):
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

@measure_router.post("/")
async def create_measure(request: CreateMeasureRequest, current_user: dict = Depends(get_current_user)):
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
async def get_measures(skip: int = 0, limit: int = 100, current_user: dict = Depends(get_current_user)):
    measure_repo = MeasureRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    measure_service = MeasureService(measure_repo, employee_repo, audit_repo)
    
    measures = await measure_service.get_measures(skip, limit)
    return measures

@measure_router.get("/dashboard/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    measure_repo = MeasureRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    measure_service = MeasureService(measure_repo, employee_repo, audit_repo)
    
    stats = await measure_service.get_dashboard_stats()
    return stats

@measure_router.get("/employee/{employee_id}")
async def get_employee_measures(employee_id: str, current_user: dict = Depends(get_current_user)):
    measure_repo = MeasureRepository(db)
    employee_repo = EmployeeRepository(db)
    audit_repo = AuditLogRepository(db)
    measure_service = MeasureService(measure_repo, employee_repo, audit_repo)
    
    measures = await measure_service.get_employee_measures(employee_id)
    return measures

@measure_router.post("/sign")
async def sign_measure(request: SignMeasureRequest, current_user: dict = Depends(require_roles(["juridico", "rh"]))):
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
async def cancel_measure(request: CancelMeasureRequest, current_user: dict = Depends(require_roles(["juridico", "rh"]))):
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

@audit_router.get("/logs")
async def get_audit_logs(limit: int = 100, current_user: dict = Depends(require_roles(["juridico", "rh"]))):
    audit_repo = AuditLogRepository(db)
    audit_service = AuditService(audit_repo)
    
    logs = await audit_service.get_recent_logs(limit)
    return logs

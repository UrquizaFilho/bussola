from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from interfaces.routes import (
    auth_router, employee_router, measure_router, audit_router,
    team_router, document_router, user_router
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI(title="Bússola - Sistema de Gestão de Medidas Disciplinares")
app.state.db = db

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(employee_router, prefix="/employees", tags=["employees"])
api_router.include_router(measure_router, prefix="/measures", tags=["measures"])
api_router.include_router(team_router, prefix="/teams", tags=["teams"])
api_router.include_router(document_router, prefix="/documents", tags=["documents"])
api_router.include_router(audit_router, prefix="/audit", tags=["audit"])

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

@app.on_event("startup")
async def startup_event():
    from infrastructure.repositories import UserRepository, EmployeeRepository, TeamRepository
    from infrastructure.auth import get_password_hash
    import uuid
    from datetime import datetime, timezone
    
    user_repo = UserRepository(db)
    employee_repo = EmployeeRepository(db)
    team_repo = TeamRepository(db)
    
    # Criar usuários demo
    demo_users = [
        {"id": str(uuid.uuid4()), "name": "Admin RH", "email": "rh@bussola.com", "password": "senha123", "role": "rh", "manager_id": None},
        {"id": str(uuid.uuid4()), "name": "Jurídico Silva", "email": "juridico@bussola.com", "password": "senha123", "role": "juridico", "manager_id": None},
        {"id": str(uuid.uuid4()), "name": "Carlos Gerente", "email": "gerente@bussola.com", "password": "senha123", "role": "gerente", "manager_id": None},
        {"id": str(uuid.uuid4()), "name": "Ana Coordenadora", "email": "coordenador@bussola.com", "password": "senha123", "role": "coordenador", "manager_id": None},
        {"id": str(uuid.uuid4()), "name": "João Supervisor", "email": "supervisor@bussola.com", "password": "senha123", "role": "supervisor", "manager_id": None},
        {"id": str(uuid.uuid4()), "name": "Maria Colaboradora", "email": "colaborador@bussola.com", "password": "senha123", "role": "colaborador", "manager_id": None},
    ]
    
    created_users = {}
    
    for user_data in demo_users:
        existing = await user_repo.find_by_email(user_data['email'])
        if not existing:
            user_doc = {
                "id": user_data['id'],
                "name": user_data['name'],
                "email": user_data['email'],
                "password_hash": get_password_hash(user_data['password']),
                "role": user_data['role'],
                "manager_id": user_data['manager_id'],
                "team_id": None,
                "active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            await user_repo.create(user_doc)
            created_users[user_data['role']] = user_data['id']
            logger.info(f"Usuário demo criado: {user_data['email']}")
        else:
            created_users[user_data['role']] = existing['id']
    
    # Criar hierarquia de equipes
    gerente_id = created_users.get('gerente')
    coordenador_id = created_users.get('coordenador')
    supervisor_id = created_users.get('supervisor')
    
    if gerente_id:
        # Atualizar hierarquia: coordenador reporta ao gerente
        if coordenador_id:
            await user_repo.update(coordenador_id, {"manager_id": gerente_id})
        
        # supervisor reporta ao coordenador
        if supervisor_id and coordenador_id:
            await user_repo.update(supervisor_id, {"manager_id": coordenador_id})
        
        # Criar equipes
        team_gerente = await team_repo.find_all({"manager_id": gerente_id})
        if not team_gerente:
            team_doc = {
                "id": str(uuid.uuid4()),
                "name": "Equipe Gerência",
                "manager_id": gerente_id,
                "manager_name": "Carlos Gerente",
                "parent_team_id": None,
                "level": "gerente",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            await team_repo.create(team_doc)
            logger.info("Equipe de Gerência criada")
    
    # Criar colaboradores demo
    demo_employees = [
        {
            "id": str(uuid.uuid4()),
            "name": "Pedro Santos",
            "cpf": "111.222.333-44",
            "email": "pedro.santos@empresa.com",
            "department": "Operações",
            "position": "Assistente",
            "admission_date": "2024-01-15T00:00:00Z",
            "supervisor_id": supervisor_id,
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Juliana Costa",
            "cpf": "555.666.777-88",
            "email": "juliana.costa@empresa.com",
            "department": "Operações",
            "position": "Assistente",
            "admission_date": "2024-02-01T00:00:00Z",
            "supervisor_id": supervisor_id,
        }
    ]
    
    for emp_data in demo_employees:
        existing = await employee_repo.find_by_cpf(emp_data['cpf'])
        if not existing:
            emp_doc = {
                **emp_data,
                "team_id": None,
                "active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            await employee_repo.create(emp_doc)
            logger.info(f"Colaborador demo criado: {emp_data['name']}")

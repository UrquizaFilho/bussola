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
    from infrastructure.repositories import UserRepository
    from infrastructure.auth import get_password_hash
    import uuid
    from datetime import datetime, timezone
    
    user_repo = UserRepository(db)
    
    demo_users = [
        {"id": str(uuid.uuid4()), "name": "Admin RH", "email": "rh@bussola.com", "password": "senha123", "role": "rh"},
        {"id": str(uuid.uuid4()), "name": "Jurídico", "email": "juridico@bussola.com", "password": "senha123", "role": "juridico"},
        {"id": str(uuid.uuid4()), "name": "Gestor", "email": "gestor@bussola.com", "password": "senha123", "role": "gerente"},
    ]
    
    for user_data in demo_users:
        existing = await user_repo.find_by_email(user_data['email'])
        if not existing:
            user_doc = {
                "id": user_data['id'],
                "name": user_data['name'],
                "email": user_data['email'],
                "password_hash": get_password_hash(user_data['password']),
                "role": user_data['role'],
                "active": True,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            await user_repo.create(user_doc)
            logger.info(f"Usuário demo criado: {user_data['email']}")

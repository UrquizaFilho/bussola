from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from infrastructure.auth import decode_access_token
from infrastructure.repositories import UserRepository
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional
import os

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
    
    return payload

def require_roles(allowed_roles: list):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user['role'] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado: permissão insuficiente"
            )
        return current_user
    return role_checker

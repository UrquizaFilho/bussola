from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from datetime import datetime
import uuid

class BaseRepository:
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        self.db = db
        self.collection = db[collection_name]
    
    async def create(self, document: dict) -> dict:
        document['_id'] = document.get('id', str(uuid.uuid4()))
        document['id'] = document['_id']
        await self.collection.insert_one(document)
        del document['_id']
        return document
    
    async def find_by_id(self, id: str) -> Optional[dict]:
        doc = await self.collection.find_one({"id": id}, {"_id": 0})
        return doc
    
    async def find_all(self, filter: dict = {}, skip: int = 0, limit: int = 100) -> List[dict]:
        cursor = self.collection.find(filter, {"_id": 0}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def update(self, id: str, update_data: dict) -> Optional[dict]:
        result = await self.collection.find_one_and_update(
            {"id": id},
            {"$set": update_data},
            return_document=True,
            projection={"_id": 0}
        )
        return result
    
    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"id": id})
        return result.deleted_count > 0
    
    async def count(self, filter: dict = {}) -> int:
        return await self.collection.count_documents(filter)

class UserRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "users")
    
    async def find_by_email(self, email: str) -> Optional[dict]:
        return await self.collection.find_one({"email": email}, {"_id": 0})

class EmployeeRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "employees")
    
    async def find_by_cpf(self, cpf: str) -> Optional[dict]:
        return await self.collection.find_one({"cpf": cpf}, {"_id": 0})

class MeasureRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "measures")
    
    async def find_by_employee(self, employee_id: str) -> List[dict]:
        cursor = self.collection.find({"employee_id": employee_id}, {"_id": 0}).sort("applied_at", -1)
        return await cursor.to_list(length=1000)
    
    async def find_recent(self, limit: int = 10) -> List[dict]:
        cursor = self.collection.find({}, {"_id": 0}).sort("applied_at", -1).limit(limit)
        return await cursor.to_list(length=limit)

class AuditLogRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "audit_logs")
    
    async def find_recent(self, limit: int = 100) -> List[dict]:
        cursor = self.collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit)
        return await cursor.to_list(length=limit)

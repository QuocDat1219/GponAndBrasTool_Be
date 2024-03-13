from fastapi import APIRouter, HTTPException
from models.systemModel import System
from config.db import conn
from schemas.systemDeviceSchemas import serializeDict, serializeList
from bson import ObjectId
systemRoutes = APIRouter()

@systemRoutes.post("/api/system/")
async def create_system(system: System):
    try:
        created_system = conn.demo.system.insert_one(dict(system))
        if created_system:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500,detail="error")


@systemRoutes.get("/api/system/")
async def get_all_system():
    systems = serializeList(conn.demo.system.find())
    return systems

@systemRoutes.get("/api/system/{id}")
async def get_system_by_id(id):
    device = serializeDict(conn.demo.system.find_one({"_id": ObjectId(id)}))
    return device

@systemRoutes.put("/api/system/{id}")
async def update_system(id, system: System):
    try:
        conn.demo.system.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(system)}
        )
        updatedSystem = serializeDict(conn.demo.system.find_one({"_id": ObjectId(id)}))
        if updatedSystem:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
            return HTTPException(status_code=500,detail="error")
        
@systemRoutes.delete("/api/system/{id}")
async def delete_system(id):
    try:
        deleted_system = conn.demo.system.delete_one({"_id": ObjectId(id)})
        if deleted_system.deleted_count == 1:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")
 
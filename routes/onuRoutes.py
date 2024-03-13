from fastapi import APIRouter, HTTPException
from models.onuModel import Onu
from config.db import conn
from schemas.onuSchemas import serializeDict,serializeList
from bson import ObjectId

onuRoutes = APIRouter()

@onuRoutes.post("/api/onu/")
async def create_onu(onu: Onu):
    try:
        created_onu = conn.demo.onu.insert_one(dict(onu))
        if created_onu:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")


@onuRoutes.get("/api/onu/")
async def get_all_onu():
    try:
        all_onu = serializeList(conn.demo.onu.find())
        return all_onu
    except:
        return HTTPException(status_code=500, detail="error")
    
    
@onuRoutes.get("/api/onu/{id}")
async def get_onu_by_id(id):
    try:
        onu = serializeDict(conn.demo.onu.find_one({"_id": ObjectId(id)}))
        return onu
    except:
        return HTTPException(status_code=500, detail="error")
        
@onuRoutes.put("/api/onu/{id}")
async def update_onu(id, onu: Onu):
    try:
        conn.demo.onu.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(onu)}
        )
        updated_onu = serializeDict(conn.demo.onu.find_one({"_id": ObjectId(id)}))
        if updated_onu:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error") 

@onuRoutes.delete("/api/onu/{id}")
async def delete_onu(id):
    try:
        deleted_onu = conn.demo.onu.delete_one({"_id": ObjectId(id)})
        if deleted_onu.deleted_count > 0:
           return HTTPException(status_code=200, detail="success")
        else:
           return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")
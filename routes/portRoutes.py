from fastapi import APIRouter, HTTPException
from models.portModel import Port
from config.db import conn
from schemas.portSchemas import serializeDict,serializeList
from bson import ObjectId

portRoutes = APIRouter()

@portRoutes.post("/api/port/")
async def create_port(port: Port):
    try:
        created_port = conn.demo.port.insert_one(dict(port))
        if created_port:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")


@portRoutes.get("/api/port/")
async def get_all_port():
    try:
        all_port = serializeList(conn.demo.port.find())
        return all_port
    except:
        return HTTPException(status_code=500, detail="error")
    
    
@portRoutes.get("/api/port/{id}")
async def get_port_by_id(id):
    try:
        port = serializeDict(conn.demo.port.find_one({"_id": ObjectId(id)}))
        return port
    except:
        return HTTPException(status_code=500, detail="error")
        
@portRoutes.put("/api/port/{id}")
async def update_port(id, port: Port):
    try:
        conn.demo.port.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(port)}
        )
        updated_port = serializeDict(conn.demo.port.find_one({"_id": ObjectId(id)}))
        if updated_port:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error") 

@portRoutes.delete("/api/port/{id}")
async def delete_port(id):
    try:
        deleted_port = conn.demo.port.delete_one({"_id": ObjectId(id)})
        if deleted_port.deleted_count > 0:
           return HTTPException(status_code=200, detail="success")
        else:
           return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")
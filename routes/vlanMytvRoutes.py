from fastapi import APIRouter, HTTPException
from models.vlanMytvModel import VlanMytv
from config.db import conn
from schemas.vlanMytvSchemas import serializeDict,serializeList
from bson import ObjectId

vlanMytvRoutes = APIRouter()

@vlanMytvRoutes.post("/api/vlanmytv/")
async def create_vlanMytv(vlanMytv: VlanMytv):
    try:
        created_vlanMytv = conn.demo.vlanmytv.insert_one(dict(vlanMytv))
        if created_vlanMytv:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.vlanmytv.find())})
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")


@vlanMytvRoutes.get("/api/vlanmytv/")
async def get_all_vlanMytv():
    try:
        all_vlanMytv = serializeList(conn.demo.vlanmytv.find())
        return all_vlanMytv
    except:
        return HTTPException(status_code=500, detail="error")
    
    
@vlanMytvRoutes.get("/api/vlanmytv/{id}")
async def get_vlanMytv_by_id(id):
    try:
        vlanMytv = serializeDict(conn.demo.vlanmytv.find_one({"_id": ObjectId(id)}))
        return vlanMytv
    except:
        return HTTPException(status_code=500, detail="error")
        
@vlanMytvRoutes.put("/api/vlanmytv/{id}")
async def update_vlanMytv(id, vlanMytv: VlanMytv):
    try:
        conn.demo.vlanMytv.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(vlanMytv)}
        )
        updated_vlanMytv = serializeDict(conn.demo.vlanmytv.find_one({"_id": ObjectId(id)}))
        if updated_vlanMytv:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.vlanmytv.find())})
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error") 

@vlanMytvRoutes.delete("/api/vlanmytv/{id}")
async def delete_vlanMytv(id):
    try:
        deleted_vlanMytv = conn.demo.vlanmytv.delete_one({"_id": ObjectId(id)})
        if deleted_vlanMytv.deleted_count > 0:
           return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.vlanmytv.find())})
        else:
           return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")
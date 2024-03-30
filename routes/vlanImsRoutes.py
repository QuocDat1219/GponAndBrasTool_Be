from fastapi import APIRouter, HTTPException
from models.vlanImsModel import VlanIMS
from config.db import conn
from schemas.vlanImsSchemas import serializeDict,serializeList
from bson import ObjectId

vlanImsRoutes = APIRouter()

@vlanImsRoutes.post("/api/vlanims/")
async def create_vlanIms(vlanIms: VlanIMS):
    try:
        created_vlanIms = conn.demo.vlanims.insert_one(dict(vlanIms))
        if created_vlanIms:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.vlanims.find())})
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")


@vlanImsRoutes.get("/api/vlanims/")
async def get_all_vlanIms():
    try:
        all_vlanIms = serializeList(conn.demo.vlanims.find())
        return all_vlanIms
    except:
        return HTTPException(status_code=500, detail="error")
    
    
@vlanImsRoutes.get("/api/vlanims/{id}")
async def get_vlanIms_by_id(id):
    try:
        vlanIms = serializeDict(conn.demo.vlanims.find_one({"_id": ObjectId(id)}))
        return vlanIms
    except:
        return HTTPException(status_code=500, detail="error")
        
@vlanImsRoutes.put("/api/vlanims/{id}")
async def update_vlanIms(id, vlanIms: VlanIMS):
    try:
        conn.demo.vlanims.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(vlanIms)}
        )
        updated_vlanIms = serializeDict(conn.demo.vlanims.find_one({"_id": ObjectId(id)}))
        if updated_vlanIms:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.vlanims.find())})
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error") 

@vlanImsRoutes.delete("/api/vlanims/{id}")
async def delete_vlanIms(id):
    try:
        deleted_vlanIms = conn.demo.vlanims.delete_one({"_id": ObjectId(id)})
        if deleted_vlanIms.deleted_count > 0:
           return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.vlanims.find())})
        else:
           return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")
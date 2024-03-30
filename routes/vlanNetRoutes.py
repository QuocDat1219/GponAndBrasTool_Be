from fastapi import APIRouter, HTTPException
from models.vlanNetModel import VlanNet
from config.db import conn
from schemas.vlanNetSchemas import serializeDict,serializeList
from bson import ObjectId

vlanNetRoutes = APIRouter()

@vlanNetRoutes.post("/api/vlannet/")
async def create_vlanNet(vlanNet: VlanNet):
    try:
        created_vlanNet = conn.demo.vlanNet.insert_one(dict(vlanNet))
        if created_vlanNet:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.vlanNet.find())})
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})


@vlanNetRoutes.get("/api/vlannet/")
async def get_all_vlanNet():
    try:
        all_vlanNet = serializeList(conn.demo.vlanNet.find())
        return all_vlanNet
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
    
    
@vlanNetRoutes.get("/api/vlannet/{id}")
async def get_vlanNet_by_id(id):
    try:
        vlanNet = serializeDict(conn.demo.vlanNet.find_one({"_id": ObjectId(id)}))
        return vlanNet
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
        
@vlanNetRoutes.put("/api/vlannet/{id}")
async def update_vlanNet(id, vlanNet: VlanNet):
    try:
        conn.demo.vlanNet.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(vlanNet)}
        )
        updated_vlanNet = serializeDict(conn.demo.vlanNet.find_one({"_id": ObjectId(id)}))
        if updated_vlanNet:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.vlanNet.find())})
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"}) 

@vlanNetRoutes.delete("/api/vlannet/{id}")
async def delete_vlanNet(id):
    try:
        deleted_vlanNet = conn.demo.vlanNet.delete_one({"_id": ObjectId(id)})
        if deleted_vlanNet.deleted_count > 0:
           return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.vlanNet.find())})
        else:
           return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
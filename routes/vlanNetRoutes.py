from fastapi import APIRouter, HTTPException, Depends
from models.vlanNetModel import VlanNet
from config.db import conn
from schemas.vlanNetSchemas import serializeDict,serializeList
from bson import ObjectId
from auth.jwt_bearer import jwtBearer
vlanNetRoutes = APIRouter()

@vlanNetRoutes.post("/api/vlannet/",dependencies=[Depends(jwtBearer())])
async def create_vlanNet(vlanNet: VlanNet):
    try:
        created_vlanNet = conn.gponbrastool.vlanNet.insert_one(dict(vlanNet))
        if created_vlanNet:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.gponbrastool.vlanNet.find())})
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})


@vlanNetRoutes.get("/api/vlannet/",dependencies=[Depends(jwtBearer())])
async def get_all_vlanNet():
    try:
        all_vlanNet = serializeList(conn.gponbrastool.vlanNet.find())
        return all_vlanNet
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
    
    
@vlanNetRoutes.get("/api/vlannet/{id}",dependencies=[Depends(jwtBearer())])
async def get_vlanNet_by_id(id):
    try:
        vlanNet = serializeDict(conn.gponbrastool.vlanNet.find_one({"_id": ObjectId(id)}))
        return vlanNet
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
        
@vlanNetRoutes.put("/api/vlannet/{id}",dependencies=[Depends(jwtBearer())])
async def update_vlanNet(id, vlanNet: VlanNet):
    try:
        conn.gponbrastool.vlanNet.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(vlanNet)}
        )
        updated_vlanNet = serializeDict(conn.gponbrastool.vlanNet.find_one({"_id": ObjectId(id)}))
        if updated_vlanNet:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.gponbrastool.vlanNet.find())})
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"}) 

@vlanNetRoutes.delete("/api/vlannet/{id}",dependencies=[Depends(jwtBearer())])
async def delete_vlanNet(id):
    try:
        deleted_vlanNet = conn.gponbrastool.vlanNet.delete_one({"_id": ObjectId(id)})
        if deleted_vlanNet.deleted_count > 0:
           return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.gponbrastool.vlanNet.find())})
        else:
           return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
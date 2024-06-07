from fastapi import APIRouter, HTTPException, Depends
from models.vlanImsModel import VlanIMS
from config.db import conn
from schemas.vlanImsSchemas import serializeDict,serializeList
from bson import ObjectId
from auth.jwt_bearer import jwtBearer
vlanImsRoutes = APIRouter()

@vlanImsRoutes.post("/api/vlanims/",dependencies=[Depends(jwtBearer())])
async def create_vlanIms(vlanIms: VlanIMS):
    try:
        created_vlanIms = conn.gponbrastool.vlanims.insert_one(dict(vlanIms))
        if created_vlanIms:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.gponbrastool.vlanims.find())})
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})


@vlanImsRoutes.get("/api/vlanims/",dependencies=[Depends(jwtBearer())])
async def get_all_vlanIms():
    try:
        all_vlanIms = serializeList(conn.gponbrastool.vlanims.find())
        return all_vlanIms
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
    
    
@vlanImsRoutes.get("/api/vlanims/{id}",dependencies=[Depends(jwtBearer())])
async def get_vlanIms_by_id(id):
    try:
        vlanIms = serializeDict(conn.gponbrastool.vlanims.find_one({"_id": ObjectId(id)}))
        return vlanIms
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
        
@vlanImsRoutes.put("/api/vlanims/{id}",dependencies=[Depends(jwtBearer())])
async def update_vlanIms(id, vlanIms: VlanIMS):
    try:
        conn.gponbrastool.vlanims.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(vlanIms)}
        )
        updated_vlanIms = serializeDict(conn.gponbrastool.vlanims.find_one({"_id": ObjectId(id)}))
        if updated_vlanIms:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.gponbrastool.vlanims.find())})
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"}) 

@vlanImsRoutes.delete("/api/vlanims/{id}",dependencies=[Depends(jwtBearer())])
async def delete_vlanIms(id):
    try:
        deleted_vlanIms = conn.gponbrastool.vlanims.delete_one({"_id": ObjectId(id)})
        if deleted_vlanIms.deleted_count > 0:
           return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.gponbrastool.vlanims.find())})
        else:
           return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
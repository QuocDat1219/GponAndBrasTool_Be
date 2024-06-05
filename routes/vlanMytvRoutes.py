from fastapi import APIRouter, HTTPException, Depends
from models.vlanMytvModel import VlanMytv
from config.db import conn
from schemas.vlanMytvSchemas import serializeDict,serializeList
from bson import ObjectId
from auth.jwt_bearer import jwtBearer

vlanMytvRoutes = APIRouter()

@vlanMytvRoutes.post("/api/vlanmytv/",dependencies=[Depends(jwtBearer())])
async def create_vlanMytv(vlanMytv: VlanMytv):
    try:
        created_vlanMytv = conn.demo.vlanmytv.insert_one(dict(vlanMytv))
        if created_vlanMytv:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.vlanmytv.find())})
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})


@vlanMytvRoutes.get("/api/vlanmytv/",dependencies=[Depends(jwtBearer())])
async def get_all_vlanMytv():
    try:
        all_vlanMytv = serializeList(conn.demo.vlanmytv.find())
        return all_vlanMytv
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
    
    
@vlanMytvRoutes.get("/api/vlanmytv/{id}",dependencies=[Depends(jwtBearer())])
async def get_vlanMytv_by_id(id):
    try:
        vlanMytv = serializeDict(conn.demo.vlanmytv.find_one({"_id": ObjectId(id)}))
        return vlanMytv
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
        
@vlanMytvRoutes.put("/api/vlanmytv/{id}",dependencies=[Depends(jwtBearer())])
async def update_vlanMytv(id, vlanMytv: VlanMytv):
    try:
        conn.demo.vlanmytv.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(vlanMytv)}
        )
        updated_vlanMytv = serializeDict(conn.demo.vlanmytv.find_one({"_id": ObjectId(id)}))
       
        if updated_vlanMytv:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.vlanmytv.find())})
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"}) 

@vlanMytvRoutes.delete("/api/vlanmytv/{id}",dependencies=[Depends(jwtBearer())])
async def delete_vlanMytv(id):
    try:
        deleted_vlanMytv = conn.demo.vlanmytv.delete_one({"_id": ObjectId(id)})
        if deleted_vlanMytv.deleted_count > 0:
           return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.vlanmytv.find())})
        else:
           return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
from fastapi import APIRouter, HTTPException, Depends
from models.shelfDeviceModel import Shelf
from config.db import conn
from schemas.shelfDeviceSchemas import serializeDict, serializeList
from bson import ObjectId
from auth.jwt_bearer import jwtBearer

shelfRoutes = APIRouter()

@shelfRoutes.post("/api/shelf/",dependencies=[Depends(jwtBearer())])
async def create_shelf(shelf: Shelf):
    try:
        created_shelf = conn.gponbrastool.shelf.insert_one(dict(shelf))
        if created_shelf:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})


@shelfRoutes.get("/api/shelf/",dependencies=[Depends(jwtBearer())])
async def get_all_shelf():
    try:
        all_shelf = serializeList(conn.gponbrastool.shelf.find())
        return all_shelf
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
    
    
@shelfRoutes.get("/api/shelf/{id}",dependencies=[Depends(jwtBearer())])
async def get_shelf_by_id(id):
    try:
        shelf = serializeDict(conn.gponbrastool.shelf.find_one({"_id": ObjectId(id)}))
        return shelf
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
        
@shelfRoutes.put("/api/shelf/{id}",dependencies=[Depends(jwtBearer())])
async def update_shelf(id, shelf:Shelf):
    try:
        conn.gponbrastool.shelf.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(shelf)}
        )
        updated_shelf = serializeDict(conn.gponbrastool.shelf.find_one({"_id": ObjectId(id)}))
        if updated_shelf:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"}) 

@shelfRoutes.delete("/api/shelf/{id}",dependencies=[Depends(jwtBearer())])
async def delete_shelf(id):
    try:
        deleted_shelf = conn.gponbrastool.shelf.delete_one({"_id": ObjectId(id)})
        if deleted_shelf.deleted_count > 0:
           return HTTPException(status_code=200, detail="success")
        else:
           return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})
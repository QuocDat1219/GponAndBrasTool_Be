from fastapi import APIRouter, HTTPException
from models.shelfDeviceModel import Shelf
from config.db import conn
from schemas.shelfDeviceSchemas import serializeDict, serializeList
from bson import ObjectId

shelfRoutes = APIRouter()

@shelfRoutes.post("/api/shelf/")
async def create_shelf(shelf: Shelf):
    try:
        created_shelf = conn.demo.shelf.insert_one(dict(shelf))
        if created_shelf:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")


@shelfRoutes.get("/api/shelf/")
async def get_all_shelf():
    try:
        all_shelf = serializeList(conn.demo.shelf.find())
        return all_shelf
    except:
        return HTTPException(status_code=500, detail="error")
    
    
@shelfRoutes.get("/api/shelf/{id}")
async def get_shelf_by_id(id):
    try:
        shelf = serializeDict(conn.demo.shelf.find_one({"_id": ObjectId(id)}))
        return shelf
    except:
        return HTTPException(status_code=500, detail="error")
        
@shelfRoutes.put("/api/shelf/{id}")
async def update_shelf(id, shelf:Shelf):
    try:
        conn.demo.shelf.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(shelf)}
        )
        updated_shelf = serializeDict(conn.demo.shelf.find_one({"_id": ObjectId(id)}))
        if updated_shelf:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error") 

@shelfRoutes.delete("/api/shelf/{id}")
async def delete_shelf(id):
    try:
        deleted_shelf = conn.demo.shelf.delete_one({"_id": ObjectId(id)})
        if deleted_shelf.deleted_count > 0:
           return HTTPException(status_code=200, detail="success")
        else:
           return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")
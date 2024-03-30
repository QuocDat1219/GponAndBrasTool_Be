from fastapi import APIRouter, HTTPException
from models.thietbi import ThietBi
from config.db import conn
from schemas.thietbiSchemas import serializeDict, serializeList
from bson import ObjectId

thietbiRoutes = APIRouter()

@thietbiRoutes.post("/api/thietbi/")
async def create_thietbi(thietbi: ThietBi):
    try:
        create_thietbi = conn.demo.thietbi.insert_one(dict(thietbi))
        if create_thietbi:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.thietbi.find())})
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"}) 

@thietbiRoutes.get("/api/thietbi/{loaithietbi}")
async def get_thietbi_by_loai_thiet_bi(loaithietbi: str):
    try:
        # Tìm kiếm tất cả các thiết bị có loại thiết bị là loaithietbi
        thietbi_list = list(conn.demo.thietbi.find({"loaithietbi": loaithietbi}))

        if not thietbi_list:
            return []
        return serializeList(thietbi_list)
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=str(e))
    
@thietbiRoutes.get("/api/thietbi/")
async def get_all_thietbi():
    try:
        # Tìm kiếm tất cả các thiết bị có loại thiết bị là loaithietbi
        thietbi_list = list(conn.demo.thietbi.find())

        if not thietbi_list:
            return []
        return serializeList(thietbi_list)
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=str(e))
    
@thietbiRoutes.get("/api/thietbi/id/{id}")
async def get_thietbi_by_id(id):
    thietbi = serializeDict(conn.demo.thietbi.find_one({"_id": ObjectId(id)}))
    print(thietbi)
    return thietbi

@thietbiRoutes.put("/api/thietbi/{id}")
async def update_thietbi(id, thietbi: ThietBi):
    try:
        conn.demo.thietbi.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(thietbi)})
        updated_thietbi = serializeDict(conn.demo.thietbi.find_one({"_id": ObjectId(id)}))
        if updated_thietbi:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.thietbi.find())})
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})

@thietbiRoutes.delete("/api/thietbi/{id}")
async def delete_thietbi(id):
    try:
        deleted_thietbi = conn.demo.thietbi.delete_one({"_id": ObjectId(id)})
        if deleted_thietbi.deleted_count == 1:
            return HTTPException(status_code=200, detail={"msg": "success", "data": serializeList(conn.demo.thietbi.find())})
        else:
            return HTTPException(status_code=500, detail={"msg": "error"})
    except:
        return HTTPException(status_code=500, detail={"msg": "error"})

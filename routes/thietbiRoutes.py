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
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error") 

@thietbiRoutes.get("/api/thietbi/{tenthietbi}")
async def get_all_thietbi():
    thietbi_list = [serializeDict(thietbi) for thietbi in conn.demo.thietbi.find()]
    return thietbi_list

@thietbiRoutes.get("/api/thietbi/{id}")
async def get_thietbi_by_id(id):
    thietbi = serializeDict(conn.demo.thietbi.find_one({"_id": ObjectId(id)}))
    return thietbi

@thietbiRoutes.put("/api/thietbi/{id}")
async def update_thietbi(id, thietbi: LoaiThietBi):
    try:
        conn.demo.thietbi.find_one_and_update({"_id": ObjectId(id)}, {"$set": thietbi.dict()})
        updated_thietbi = serializeDict(conn.demo.thietbi.find_one({"_id": ObjectId(id)}))
        if updated_thietbi:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")

@thietbiRoutes.delete("/api/thietbi/{id}")
async def delete_thietbi(id):
    try:
        deleted_thietbi = conn.demo.thietbi.delete_one({"_id": ObjectId(id)})
        if deleted_thietbi.deleted_count == 1:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")

from fastapi import APIRouter, HTTPException
from models.deviceModel import Device
from config.db import conn
from schemas.deviceSchemas import serializeDict,serializeList
from bson import ObjectId
deviceRoutes = APIRouter()

@deviceRoutes.post("/api/device/")
async def create_device(device:Device):
    try:
        created_device = conn.demo.device.insert_one(dict(device))
        if created_device:
            return HTTPException(status_code=200, detail=f"success")
        else:
            return HTTPException(status_code=500, detail=f"error")
    except:
            return HTTPException(status_code=500, detail=f"error")


@deviceRoutes.get("/api/device/")
async def get_all_device():
    devices = serializeList(conn.demo.device.find())
    return devices

@deviceRoutes.get("/api/device/{id}")
async def get_device_by_id(id):
    device = serializeDict(conn.demo.device.find_one({"_id": ObjectId(id)}))
    return device

@deviceRoutes.put("/api/device/{id}")
async def update_device(id, device:Device):
    try:
        conn.demo.device.find_one_and_update({"_id": ObjectId(id)}, {
            "$set": dict(device)
        })
        updatedDevice = serializeDict(conn.demo.device.find_one({"_id": ObjectId(id)}))
        if updatedDevice:
            return HTTPException(status_code=200, detail="success")
        else:
            return HTTPException(status_code=500, detail="error")
    except:
        return HTTPException(status_code=500, detail="error")

@deviceRoutes.delete("/api/device/{id}")
async def delete_device(id):
    try:
        deleted_device = conn.demo.device.delete_one({"_id": ObjectId(id)})
        if deleted_device.deleted_count == 1:
            return HTTPException(status_code=200,detail="success")
        else:
            return HTTPException(status_code=500,detail="error")
    except:
        return HTTPException(status_code=500, detail="error")
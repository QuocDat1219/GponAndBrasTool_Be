from fastapi import APIRouter, HTTPException
from models.ipAddressModel import IpAddress
from config.db import conn
from schemas.ipAddressSchemas import serializeDict, serializeList
from bson import ObjectId
from service.sshBras import phan_loai_thiet_bi
ipAddressRoutes = APIRouter()

# Tạo mới địa chỉ ip kết nối bras

@ipAddressRoutes.post('/api/ipaddress/')
async def create_ip_address(ipAddress:IpAddress):
    try:
        createdIp = conn.demo.ipaddress.insert_one(dict(ipAddress))
        if createdIp:
            return HTTPException(status_code=200, detail={ "msg" : f"success", "data": serializeList(conn.demo.ipaddress.find())})
        else:
            return HTTPException(status_code=500,detail=f"error")
    except:
        return HTTPException(status_code=500,detail=f"error")
# Lấy danh sách ip address

@ipAddressRoutes.get('/api/ipaddress/')
async def get_all_ip_addresses():
    allIp = serializeList(conn.demo.ipaddress.find())
    return allIp

@ipAddressRoutes.get("/api/ipddress/{id}")
async def get_ip_address(id):
    ipAddress = serializeDict(conn.demo.ipaddress.find_one({"_id": ObjectId(id)}))
    return ipAddress

@ipAddressRoutes.delete('/api/ipaddress/{id}')
async def delete_ip_address(id):
    try:
        deleted_id = conn.demo.ipaddress.delete_one({"_id": ObjectId(id)})
        if deleted_id.deleted_count == 1:
            return HTTPException(status_code = 200, detail=f"success")
        else:
            return HTTPException(status_code = 500, detail=f"error")
    except:
        return HTTPException(status_code = 500, detail=f"error")

@ipAddressRoutes.put("/api/ipaddress/{id}")
async def update_ip_address(id, ipAddress: IpAddress):
    try:
        conn.demo.ipaddress.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(ipAddress)}
        )
        updatedIpAddress = conn.demo.ipaddress.find_one({"_id": ObjectId(id)})
        if updatedIpAddress:
            return HTTPException(status_code=200, detail=f"success")
        else:
            return HTTPException(status_code=500, detail=f"error")
    except:
        return HTTPException(status_code=500, detail=f"error")
    
@ipAddressRoutes.post('/api/bras/custom')
async def custom_bras(data: dict):
        phan_loai_thiet_bi(data['commands'], data['device_types'], data["thongso1"],data["thongso2"],data["thongso3"])

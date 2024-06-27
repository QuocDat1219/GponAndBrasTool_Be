from fastapi import APIRouter, HTTPException, Depends, Query
from models.ipAddressModel import IpAddress
from config.db import conn
from schemas.ipAddressSchemas import serializeDict, serializeList
from bson import ObjectId
from auth.jwt_bearer import jwtBearer
ipAddressRoutes = APIRouter()
    
# Tạo mới địa chỉ ip kết nối bras

@ipAddressRoutes.post('/api/ipaddress/',dependencies=[Depends(jwtBearer())])
async def create_ip_address(ipAddress:IpAddress):
    try:
        createdIp = conn.gponbrastool.ipaddress.insert_one(dict(ipAddress))
        if createdIp:
            return HTTPException(status_code=200, detail={ "msg" : f"success", "data": serializeList(conn.gponbrastool.ipaddress.find())})
        else:
            return HTTPException(status_code=500, detail={ "msg" : f"error"})
    except:
        return HTTPException(status_code=500,detail={ "msg" : f"error"})
# Lấy danh sách ip address

@ipAddressRoutes.get('/api/ipaddress/',dependencies=[Depends(jwtBearer())])
async def get_all_ip_addresses():
    allIp = serializeList(conn.gponbrastool.ipaddress.find())
    return allIp

@ipAddressRoutes.get("/api/ipddress/{id}",dependencies=[Depends(jwtBearer())])
async def get_ip_address(id):
    ipAddress = conn.gponbrastool.ipaddress.find_one({"_id": ObjectId(id)})
    if ipAddress:
        return serializeDict(ipAddress)
    else:
        return HTTPException(status_code=500,detail={ "msg" : f"Không tìm thấy dữ liệu"})

# Tìm kiếm gần đúng
@ipAddressRoutes.get("/api/ipaddress/find", dependencies=[Depends(jwtBearer())])
async def find_ip_address(ip: str = Query(..., description="Ip cần tìm")):
    ipAddresses = serializeList(conn.gponbrastool.ipaddress.find({"ipaddress": {"$regex": ip, "$options": "i"}}))
    return ipAddresses

@ipAddressRoutes.delete('/api/ipaddress/{id}',dependencies=[Depends(jwtBearer())])
async def delete_ip_address(id):
    try:
        deleted_id = conn.gponbrastool.ipaddress.delete_one({"_id": ObjectId(id)})
        if deleted_id.deleted_count == 1:
            return HTTPException(status_code = 200, detail={ "msg" : f"success", "data": serializeList(conn.gponbrastool.ipaddress.find())})
        else:
            return HTTPException(status_code = 500,detail={ "msg" : f"error"})
    except:
        return HTTPException(status_code = 500, detail={ "msg" : f"error"})

@ipAddressRoutes.put("/api/ipaddress/{id}",dependencies=[Depends(jwtBearer())])
async def update_ip_address(id, ipAddress: IpAddress):
    try:
        conn.gponbrastool.ipaddress.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(ipAddress)}
        )
        updatedIpAddress = conn.gponbrastool.ipaddress.find_one({"_id": ObjectId(id)})
        if updatedIpAddress:
            return HTTPException(status_code=200, detail={ "msg" : f"success", "data": serializeList(conn.gponbrastool.ipaddress.find())})
        else:
            return HTTPException(status_code=500,detail={ "msg" : f"error"})
    except:
        return HTTPException(status_code=500,detail={ "msg" : f"error"})
    





from fastapi import APIRouter, HTTPException, WebSocket
from models.ipAddressModel import IpAddress
from config.db import conn
from schemas.ipAddressSchemas import serializeDict, serializeList
from bson import ObjectId
from service.gponZTE import ssh_bras_gpon_zte_command
from service.gponMiniZTE import ssh_bras_gpon_mini_zte_command
from service.gponHW import ssh_bras_gpon_hw_command
from service.gponALU import ssh_bras_gpon_alu_command
ipAddressRoutes = APIRouter()

    
@ipAddressRoutes.post('/api/bras/custom')
async def custom_bras(data: dict):  # Thêm đối số mặc định cho websocket
    loat_thiet_bi = data["device_types"]
    if loat_thiet_bi == "GPON ZTE":
        ssh_bras_gpon_zte_command(data['commands'], data["card"], data["port"], data["onu"], data["slid"])
    elif loat_thiet_bi == "GPON MINI ZTE":
        ssh_bras_gpon_mini_zte_command(data['commands'], data["card"], data["port"], data["onu"], data["slid"])
    elif loat_thiet_bi == "GPON HW":
        ssh_bras_gpon_hw_command(data['commands'], data["card"], data["port"], data["onu"], data["slid"])
    elif loat_thiet_bi == "GPON ALU":
        ssh_bras_gpon_alu_command(data['commands'], data["card"], data["port"], data["onu"], data["slid"])
    else:
        raise HTTPException(status_code=400, detail="Thiếu thông tin cần thiết trong dữ liệu gửi đi")

    
# Tạo mới địa chỉ ip kết nối bras

@ipAddressRoutes.post('/api/ipaddress/')
async def create_ip_address(ipAddress:IpAddress):
    try:
        createdIp = conn.demo.ipaddress.insert_one(dict(ipAddress))
        if createdIp:
            return HTTPException(status_code=200, detail={ "msg" : f"success", "data": serializeList(conn.demo.ipaddress.find())})
        else:
            return HTTPException(status_code=500, detail={ "msg" : f"error"})
    except:
        return HTTPException(status_code=500,detail={ "msg" : f"error"})
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
            return HTTPException(status_code = 200, detail={ "msg" : f"success", "data": serializeList(conn.demo.ipaddress.find())})
        else:
            return HTTPException(status_code = 500,detail={ "msg" : f"error"})
    except:
        return HTTPException(status_code = 500, detail={ "msg" : f"error"})

@ipAddressRoutes.put("/api/ipaddress/{id}")
async def update_ip_address(id, ipAddress: IpAddress):
    try:
        conn.demo.ipaddress.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dict(ipAddress)}
        )
        updatedIpAddress = conn.demo.ipaddress.find_one({"_id": ObjectId(id)})
        if updatedIpAddress:
            return HTTPException(status_code=200, detail={ "msg" : f"success", "data": serializeList(conn.demo.ipaddress.find())})
        else:
            return HTTPException(status_code=500,detail={ "msg" : f"error"})
    except:
        return HTTPException(status_code=500,detail={ "msg" : f"error"})
    





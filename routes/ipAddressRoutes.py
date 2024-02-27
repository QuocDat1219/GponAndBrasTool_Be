from fastapi import APIRouter, HTTPException
from models.ipAddressModel import IpAddress
from config.db import conn
from schemas.ipAddressSchemas import serializeDict, serializeList
from bson import ObjectId
from service.sshBras import ssh_bras_command
ipAddress = APIRouter()

# Tạo mới địa chỉ ip kết nối bras

@ipAddress.post('/api/ipddress/create')
async def create_ip_address(ipAddress:IpAddress):
    try:
        createdIp = conn.demo.ipaddress.insert_one(dict(ipAddress))
        if createdIp:
            return HTTPException(status_code=200, detail=f"Thêm mới thành công!")
        else:
            return HTTPException(status_code=500,detail=f"Thêm mới không thành công!")
    except:
        return HTTPException(status_code=500,detail=f"Đã xảy ra lỗi, hãy thử lại!")
# Lấy danh sách ip address

@ipAddress.get('/api/ipddress/')
async def get_all_ip_addresses():
    allIp = serializeList(conn.demo.ipaddress.find())
    return allIp

@ipAddress.delete('/api/ipddress/delete/{id}')
async def delete_ip_address(id):
    try:
        deleted_id = conn.demo.ipaddress.delete_one({"_id": ObjectId(id)})
        if(deleted_id):
            return HTTPException(status_code = 200, detail=f"Xóa thành công!")
        else:
            return HTTPException(status_code = 400, detail=f"Không tìm thấy địa chỉ ip")
    except:
        return HTTPException(status_code = 500, detail=f"Đã xảy ra lỗi, hãy thử lại")

@ipAddress.post('/api/bras/custom')
async def custom_bras(data: dict):
    try:
        # print(data)
        ssh_bras_command(data['commands'], data['ipaddress'], data['username'], data['password'])
    except Exception as e:
        error_message = f"SSH Connection to { data.ipaddress} failed: {str(e)}"
        # self.update_output(f"\n{error_message}\n")
        print(f"Errr")

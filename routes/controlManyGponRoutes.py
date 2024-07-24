import asyncio
from fastapi import APIRouter, HTTPException, Depends
from auth.jwt_bearer import jwtBearer
from service.handleManyGpon import controlManygpon

controlManyGponRouter = APIRouter()

@controlManyGponRouter.post('/api/gpon/control_many')
async def controlGpon(data: dict):
    loai_thiet_bi = data["device_types"]
    ipaddress = data["ipaddress"]
    command_list = (data['commands'])  # Chuyển đổi chuỗi biểu diễn của list thành list thực
    card = int(data["card"])
    port = int(data["port"])
    onu = int(data["onu"])
    slid = str(data["slid"])
    vlanims = int(data["vlanims"])
    vlanmytv = int(data["vlanmytv"])
    vlannet = int(data["vlannet"])
    
    if loai_thiet_bi and ipaddress and command_list:
        results = await controlManygpon(loai_thiet_bi, ipaddress, command_list, card, port, onu, slid, vlanims, vlanmytv, vlannet)
        return {"status_code": 200, "detail": results}
    else:
        raise HTTPException(status_code=400, detail="Thiếu các tham số cần thiết")

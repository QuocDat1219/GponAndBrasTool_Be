import asyncio
from fastapi import APIRouter, HTTPException, Depends
from auth.jwt_bearer import jwtBearer
from service.gponALU import control_gpon_alu
from service.gponHW import control_gpon_hw
from service.gponMiniHW import control_gpon_minihw
from service.gponZTE import control_gpon_zte
from service.gponMiniZTE import control_gpon_minizte

controlManyGponRouter = APIRouter()

@controlManyGponRouter.post('/api/gpon/control_many')
async def controlGpon(data: dict):
    loai_thiet_bi = data["devicetype"]
    ipaddress = data["ipaddress"]
    listconfig = (data['listconfig'])  # Chuyển đổi chuỗi biểu diễn của list thành list thực
    if loai_thiet_bi and ipaddress and listconfig:
        if loai_thiet_bi == "GPON ALU":
            return await control_gpon_alu(ipaddress, listconfig)
        elif loai_thiet_bi == "GPON HW":
           return await control_gpon_hw(ipaddress, listconfig)
        elif loai_thiet_bi == "GPON MINI HW":
           return await control_gpon_minihw(ipaddress, listconfig)
        elif loai_thiet_bi == "GPON ZTE":
            return await control_gpon_zte(ipaddress, listconfig)
        elif loai_thiet_bi == "GPON MINI ZTE":
            return await control_gpon_minizte(ipaddress, listconfig)
        else:
            raise HTTPException(status_code=400, detail="Thiết bị này không được hỗ trợ")
    else:
        raise HTTPException(status_code=400, detail="Thiếu các tham số cần thiết")

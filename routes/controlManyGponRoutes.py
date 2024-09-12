import asyncio
from fastapi import APIRouter, HTTPException, Depends
from auth.jwt_bearer import jwtBearer
from service.gponALU import control_gpon_alu_list
from service.gponHW import control_gpon_hw_list
from service.gponMiniHW import control_gpon_minihw_list
from service.gponZTE import control_gpon_zte_list
from service.gponMiniZTE import control_gpon_minizte_list
from service.gponWebSocket import control_gpon_zte_ws

controlManyGponRouter = APIRouter()

@controlManyGponRouter.post('/api/gpon/control_many',dependencies=[Depends(jwtBearer())])
async def controlGpon(data: dict):
    loai_thiet_bi = data["devicetype"]
    ipaddress = data["ipaddress"]
    listconfig = (data['listconfig'])  # Chuyển đổi chuỗi biểu diễn của list thành list thực
    if loai_thiet_bi and ipaddress and listconfig:
        if loai_thiet_bi == "GPON ALU":
            return await control_gpon_alu_list(ipaddress, listconfig)
        elif loai_thiet_bi == "GPON HW":
           return await control_gpon_hw_list(ipaddress, listconfig)
        elif loai_thiet_bi == "GPON MINI HW":
           return await control_gpon_minihw_list(ipaddress, listconfig)
        elif loai_thiet_bi == "GPON ZTE":
            return await control_gpon_zte_list(ipaddress, listconfig)
        elif loai_thiet_bi == "GPON MINI ZTE":
            return await control_gpon_minizte_list(ipaddress, listconfig)
        elif loai_thiet_bi == "GPON WS ZTE":
            return await control_gpon_zte_ws(ipaddress, listconfig)
        else:
            raise HTTPException(status_code=400, detail="Thiết bị này không được hỗ trợ")
    else:
        raise HTTPException(status_code=400, detail="Thiếu các tham số cần thiết")

# import asyncio
# from fastapi import APIRouter, HTTPException, Depends
# from auth.jwt_bearer import jwtBearer
# from service.gponWebSocket import control_gpon_zte_ws

# socketRoutes = APIRouter()

# @socketRoutes.post('/api/gpon/control_socket',dependencies=[Depends(jwtBearer())])
# async def controlGpon(data: dict):
#     loai_thiet_bi = data["devicetype"]
#     ipaddress = data["ipaddress"]
#     listconfig = (data['listconfig'])  # Chuyển đổi chuỗi biểu diễn của list thành list thực
#     if loai_thiet_bi and ipaddress and listconfig:
      
#         if loai_thiet_bi == "GPON WS ZTE":
#             return await control_gpon_zte_ws(ipaddress, listconfig)
#         else:
#             raise HTTPException(status_code=400, detail="Thiết bị này không được hỗ trợ")
#     else:
#         raise HTTPException(status_code=400, detail="Thiếu các tham số cần thiết")

import asyncio
from fastapi import APIRouter, HTTPException
from service.gponZTE import ssh_bras_gpon_zte_command
from service.gponMiniZTE import ssh_bras_gpon_mini_zte_command
from service.gponHW import ssh_bras_gpon_hw_command
from service.gponALU import ssh_bras_gpon_alu_command
from service.sshBras import exploit_bras_vlg01, exploit_bras_vlg02
controlDeviceRoutes = APIRouter()

    
@controlDeviceRoutes.post('/api/gpon/control')
async def ssh_gpon(data: dict):  # Thêm đối số mặc định cho websocket
    print(data)
    loai_thiet_bi = data["device_types"]
    ipaddress = data["ipaddress"]
    commands = data['commands']
    card = int(data["card"])
    port = int(data["port"])
    onu = int(data["onu"])
    slid = int(data["slid"])
    vlanims = int(data["vlanims"])
    vlanmytv = int(data["vlanmytv"])
    vlannet = int(data["vlannet"])
    
    if loai_thiet_bi == "GPON ZTE":
        return await ssh_bras_gpon_zte_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet)
    elif loai_thiet_bi == "GPON MINI ZTE":
        return await ssh_bras_gpon_mini_zte_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet)
    elif loai_thiet_bi == "GPON HW":
        return await ssh_bras_gpon_hw_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet)
    elif loai_thiet_bi == "GPON ALU":
        return await ssh_bras_gpon_alu_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet)
    else:
        raise HTTPException(status_code=400, detail="Thiếu thông tin cần thiết trong dữ liệu gửi đi")
    
@controlDeviceRoutes.post('/api/bras/control')
async def ssh_bras(data: dict):
    sobras = data["bras"]
    
    if "bras1" in sobras:
        exploit_bras_vlg01(data["command"],data["mac"])
    if "bras2" in sobras:
        exploit_bras_vlg02(data["command"],data["mac"])
    if "bras3" in sobras:
        print("ok 3")
    if "bras1" not in sobras and "bras2" not in sobras and "bras3" not in sobras:
        return HTTPException(status_code = 500, detail={"msg": "Hãy chọn bras cần khai thác"})
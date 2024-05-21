import asyncio
from fastapi import APIRouter, HTTPException
from service.gponZTE import ssh_bras_gpon_zte_command
from service.gponMiniZTE import ssh_bras_gpon_mini_zte_command
from service.gponHW import ssh_bras_gpon_hw_command
from service.gponALU import ssh_bras_gpon_alu_command
from service.sshBras import ssh_bras_command_with_mac, ssh_bras_command_with_username, ssh_bras_command
controlDeviceRoutes = APIRouter()
               
@controlDeviceRoutes.post('/api/gpon/control')
async def ssh_gpon(data: dict):  # Thêm đối số mặc định cho websocket
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
        raise HTTPException(status_code=500, detail={"msg": "Chưa chọn loại thiết bị"})
    
@controlDeviceRoutes.post('/api/bras/control')
def ssh_bras(data: dict):
    if "command" in data and "mac" not in data and "username_bras" not in data:
        command = data["command"]
        print("aaaaaaa")
        return ssh_bras_command(command)
    elif "mac" in data and "command" in data:
        mac = data["mac"]
        command = data["command"]
        print(command)
        print(mac)
        return ssh_bras_command_with_mac(command, mac)
    elif "username_bras" in data and "command" in data:
        username = data["username_bras"]
        command = data["command"]
        print(command)
        print(username)
        return ssh_bras_command_with_username(command, username)
    else:
        raise HTTPException(status_code=400, detail={"msg": "Thiếu thông tin cần thực hiện"})



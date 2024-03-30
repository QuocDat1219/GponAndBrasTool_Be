from fastapi import APIRouter, HTTPException
from service.gponZTE import ssh_bras_gpon_zte_command
from service.gponMiniZTE import ssh_bras_gpon_mini_zte_command
from service.gponHW import ssh_bras_gpon_hw_command
from service.gponALU import ssh_bras_gpon_alu_command
from service.sshBras import exploit_bras_vlg01, exploit_bras_vlg02
controlDeviceRoutes = APIRouter()

    
@controlDeviceRoutes.post('/api/gpon/control')
async def ssh_gpon(data: dict):  # Thêm đối số mặc định cho websocket
    loat_thiet_bi = data["device_types"]
    if loat_thiet_bi == "GPON ZTE":
        ssh_bras_gpon_zte_command(data['commands'], data["card"], data["port"], data["onu"], data["slid"], data["vlanims"],data["vlanmytv"], data["vlannet"])
    elif loat_thiet_bi == "GPON MINI ZTE":
        ssh_bras_gpon_mini_zte_command(data['commands'], data["card"], data["port"], data["onu"], data["slid"], data["vlanims"],data["vlanmytv"], data["vlannet"])
    elif loat_thiet_bi == "GPON HW":
        ssh_bras_gpon_hw_command(data['commands'], data["card"], data["port"], data["onu"], data["slid"], data["vlanims"],data["vlanmytv"], data["vlannet"])
    elif loat_thiet_bi == "GPON ALU":
        ssh_bras_gpon_alu_command(data['commands'], data["card"], data["port"], data["onu"], data["slid"], data["vlanims"],data["vlanmytv"], data["vlannet"])
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
import asyncio
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from service.gponZTE import ssh_bras_gpon_zte_command
from service.gponMiniZTE import ssh_bras_gpon_mini_zte_command
from service.gponHW import ssh_bras_gpon_hw_command
from service.gponALU import ssh_bras_gpon_alu_command
from service.sshBras import ssh_bras_command_with_mac, ssh_bras_command_with_username, ssh_bras_command, clear_user_bras
from service.gponMiniHW import ssh_bras_gpon_minihw_command
from config.db import conn
from auth.jwt_bearer import jwtBearer

controlDeviceRoutes = APIRouter()
def format_command(command):
    if command == "sync_password":
        return "Xem Password đồng bộ"  
    if command == "check_mac":
        return "Xem Mac"
    if command == "status_port":
        return "Xem trạng thái port"
    if command == "view_info_onu":
        return "Xem info (GPON MINI HW && GPOM HW)"
    if command == "check_capacity":
        return "iểm tra công suất"
    if command == "check_service_port":
        return "Kiểm tra service port cho OLT HW"
    if command == "change_sync_password":
        return "Đổi Password đồng bộ"
    if command == "delete_port":
        return "Xóa Port"  
    if command == "create_dvnet":
        return "Tạo dịch vụ DV_NET"
    if command == "dv_mytv":
        return "Tạo dịch vụ DV_MYTV" 
    if command == "dv_ims":
        return "Tạo dịch vụ DV_IMS"      
    else:
        return "Chức năng chưa xác định"  
@controlDeviceRoutes.post('/api/gpon/control',dependencies=[Depends(jwtBearer())])
async def ssh_gpon(data: dict,token: str = Depends(jwtBearer())):  # Thêm đối số mặc định cho websocket
    loai_thiet_bi = data["device_types"]
    ipaddress = data["ipaddress"]
    commands = data['commands']
    card = int(data["card"])
    port = int(data["port"])
    onu = int(data["onu"])
    slid = str(data["slid"])
    vlanims = int(data["vlanims"])
    vlanmytv = int(data["vlanmytv"])
    vlannet = int(data["vlannet"])

    #Ghi lai lich su
    now = datetime.now()
    user_gpon = token["fullname"]
    command_history = format_command(commands)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    text = f"Ngày {dt_string}: Người dùng: {user_gpon}, khai thác thiết bị {loai_thiet_bi}, Ipaddress: {ipaddress}, chức năng: {command_history}. Thông số card: {card}, port: {port}, onu: {onu}, vlannet: {vlannet}, vlanims:{vlanims}, vlanmytv: {vlanmytv}"
    # Tạo đối tượng lịch sử
    history_entry = {
        "history": text,
        "status": "H",
        "created_at": dt_string
    }

    # Lưu vào database
    conn.gponbrastool.history.insert_one(history_entry)

    if loai_thiet_bi == "GPON ZTE":
        return await ssh_bras_gpon_zte_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet)
    elif loai_thiet_bi == "GPON MINI ZTE":
        return await ssh_bras_gpon_mini_zte_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet)
    elif loai_thiet_bi == "GPON HW":
        service_portnet = data["service_portnet"]
        service_portgnms = data["service_portgnms"]
        service_portims = data["service_portims"]
        return await ssh_bras_gpon_hw_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet, service_portnet, service_portgnms,service_portims)
    elif loai_thiet_bi == "GPON ALU":
        return await ssh_bras_gpon_alu_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet)
    elif loai_thiet_bi == "GPON MINI HW":
        return await ssh_bras_gpon_minihw_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet)
    else:
        raise HTTPException(status_code=500, detail={"msg": "Chưa chọn loại thiết bị"})
    
@controlDeviceRoutes.post('/api/bras/control',dependencies=[Depends(jwtBearer())])
async def ssh_bras(data: dict):
    
    command = data["command"]
    
    if "mac" not in data and "username_bras" not in data:
        return await ssh_bras_command(command)
    elif "mac" in data:
        mac = data["mac"]
        print(mac)
        return await ssh_bras_command_with_mac(command, mac)
    elif "username_bras" in data:
        username = data["username_bras"]
        
        if(command == "clear_user_bras"):
            return await clear_user_bras(command,username)
        else:
            return await ssh_bras_command_with_username(command, username)
    else:
        raise HTTPException(status_code=400, detail={"msg": "Thiếu thông tin cần thực hiện"})



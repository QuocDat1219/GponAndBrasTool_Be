import paramiko
import time
import os
import asyncio
from fastapi import HTTPException


# Lấy thông tin đăng nhập gpon
gpon_username = os.getenv("GPON_HW_USERNAME")
gpon_password = os.getenv("GPON_HW_PASSWORD")


def phan_loai_command(commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
    if commands == "sync_password":
        return ["display ont autofind all"]
    elif commands == "view_inofo_onu":
        return [f"display ont inf 0 {card} {port} {onu}"]
    # elif commands == "delete_port":
    #     return [
    #         "config",
    #         "undo service-port port 0/0/0 ont 59",
    #         "interface gpon 0/0",
    #         "ont delete  0  59"
    #     ]
    else:
        raise HTTPException(status_code=400, detail={"error": "Chức năng trên thiết bị này chưa được cập nhật"})
async def execute_command(channel, cmd):
    channel.send(cmd + '\n')
    await asyncio.sleep(0.5)
    output = channel.recv(65535).decode().strip()
    return output

async def ssh_bras_gpon_hw_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
    print(commands) 
    try:
        session = paramiko.SSHClient()
        session.load_system_host_keys()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(ipaddress, username=gpon_username, password=gpon_password, timeout=10)
        # Tạo kênh SSH
        channel = session.invoke_shell()
        # Nhận dữ liệu đầu ra ban đầu từ kênh
        output = channel.recv(65535).decode('utf-8')
        # Xác minh rằng bạn đang ở chế độ "enable"
        if '#' not in output:
            channel.send('enable\n')
            await asyncio.sleep(1)
            output = channel.recv(65535).decode('utf-8')
        # Nhận kết quả trả về từ hàm phân loại chức năng sẽ thực hiện
        command = phan_loai_command(commands, card, port, onu, slid, vlanims, vlanmytv, vlannet)
        results = []
        # Chạy lần lượt từng command
        for cmd in command:
            print(cmd)
            result = await execute_command(channel, cmd)
            results.append(result)
        return HTTPException(status_code=200, detail= results)
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
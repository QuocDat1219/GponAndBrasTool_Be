import os
import asyncio
import paramiko
import time
import os
from fastapi import HTTPException
import telnetlib3

# Lấy thông tin đăng nhập gpon
gpon_username = os.getenv("ZTE_USERNAME")
gpon_password = os.getenv("ZTE_PASSWORD")
gpon_ip = os.getenv("ZTE_IP")

def phan_loai_command(command, card, port, onu, slid, vlanims, vlanmytv, vlannet):
    if command == "change_sync_password_list":
        return ["configure terminal",
            f"interface  gpon-onu_1/{card}/{port}:{onu}",
            "sn-bind disable",
            f"registration-method pw {slid}",
            "end"
        ]
    else:
        raise HTTPException(status_code=400, detail="Lệnh trên thiết bị này chưa được cập nhật")

# Hàm thực thi lệnh Telnet và trả về kết quả
async def execute_telnet_command(reader, writer, cmd):
    writer.write(cmd.encode('ascii') + b'\n')
    await writer.drain()
    await asyncio.sleep(0.7)
    output = await reader.read(65535)
    return cmd + '\n' + output.decode('latin-1').strip()

#Sử dụng websocket
# Hàm điều khiển gpon zte tạo dãy
async def control_gpon_zte_ws(ipaddress, listconfig, manager, sid):
    try:
        # Kết nối Telnet
        reader, writer = await asyncio.open_connection(ipaddress, 23)

        # Xác thực với tên người dùng và mật khẩu
        writer.write(gpon_username.encode('ascii') + b'\n')
        await writer.drain()
        await asyncio.sleep(1)
        writer.write(gpon_password.encode('ascii') + b'\n')
        await writer.drain()
        await asyncio.sleep(1)

        results = []

        # Duyệt qua từng cấu hình trong listconfig
        for config in listconfig:
            command_list = [cmd.strip() for cmd in config["commands"].strip("[]").split(",")]
            card = config["newcard"]
            port = config["newport"]
            onu = config["newonu"]
            slid = config["slid"]
            vlanims = config.get("vlanims", 0)
            vlanmytv = config.get("vlanmytv", 0)
            vlannet = config.get("vlannet", 0)

            # Phân loại và thực thi lệnh
            for command in command_list:
                command_steps = phan_loai_command(command, card, port, onu, slid, vlanims, vlanmytv, vlannet)
                for cmd in command_steps:
                    result = await execute_telnet_command(reader, writer, cmd)
                    results.append(result)  
                    await manager.emit('command_result', {'result': result}, to=sid)  # Gửi kết quả qua WebSocket
                    print(result)

        writer.write(b'exit\n')
        await writer.drain()
        await asyncio.sleep(0.7)
        writer.write(b'y\n')
        await writer.drain()
        await asyncio.sleep(0.7)
        writer.close()
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

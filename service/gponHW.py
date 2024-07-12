import paramiko
import time
import os
import asyncio
from fastapi import HTTPException


# Lấy thông tin đăng nhập gpon
gpon_username = os.getenv("GPON_HW_USERNAME")
gpon_password = os.getenv("GPON_HW_PASSWORD")


def phan_loai_command(commands, card, port, onu, slid, vlanims, vlanmytv, vlannet, service_portnet, service_portgnms,service_portims):
    if commands == "sync_password":
        return ["display ont autofind all"]
    elif commands == "view_info_onu":
        return [f"display ont inf 0 {card} {port} {onu}"]
    elif commands == "delete_port":
        return [
            "config",
            f"undo service-port port 0/{card}/{port} ont {onu}",
            "y",
            f"interface gpon 0/{card}",
            f"ont delete {port} {onu}"
        ]
    elif commands == "create_dvnet":
        return [
                "config",
                f"interface gpon 0/{card}",
                f"ont add {port} {onu} password-auth \"{slid}\" always-on omci ont-lineprofile-id 300 ont-srvprofile-id 300 desc \"noname\"",
                "quit",
                f"service-port {service_portnet} vlan {vlannet} gpon 0/{card}/{port} ont {onu} gemport 1 multi-service user-vlan  11 tag-transform translate inbound traffic-table index 300 outbound traffic-table index 300",
                f"service-port {service_portgnms} vlan 4040 gpon 0/{card}/{port} ont {onu} gemport 5 multi-service user-vlan 4000 tag-transform translate inbound traffic-table index 300 outbound traffic-table index 300",
                "quit"
        ]
    elif commands == "dv_ims":
        return [
             "config",
                f"interface gpon 0/{card}",
                f"ont add {port} {onu} password-auth \"{slid}\" always-on omci ont-lineprofile-id 300 ont-srvprofile-id 300 desc \"noname\"",
                "quit",
                f"service-port {service_portims} vlan {vlanims} gpon 0/{card}/{port} ont {onu} gemport 3 multi-service user-vlan 13 tag-transform translate inbound traffic-table index 300 outbound  traffic-table index 300",
        ]    
    elif commands == "check_mac":
        return [f"display  mac-address  port 0/{card}/{port} ont {onu}"]
    elif commands == "check_service":
        return [f"display  service-port port 0/{card}/{port} ont {onu}"]
    elif commands == "change_sync_password":
        return ["Config",
                "interface  gpon 0/0",
                f"ont  modify {port} {onu} password {slid}",
                "quit"
        ]
    elif commands == "check_service_port":
        return [
            f"display service-port port 0/{card}/{port} ont {onu}"
        ]
    else:
        raise HTTPException(status_code=400, detail={"error": "Chức năng trên thiết bị này chưa được cập nhật"})
    
async def execute_command(channel, cmd):
    channel.send(cmd + '\n')
    await asyncio.sleep(1)
    output = channel.recv(65535).decode().strip()
    final_output = output

    # Kiểm tra nếu kết quả trả về chứa '{ <cr>||<K> }' thì gửi thêm một lần enter
    if '{ <cr>||<K> }' in output or '{ <cr>|gemport<K> }:' in output or '{ <cr>|e2e<K>|gemport<K>|sort-by<K> }' in output:
        channel.send('\n')
        await asyncio.sleep(1)
        output = channel.recv(65535).decode().strip()
        final_output += output
    
        # Kiểm tra nếu kết quả trả về chứa '---- More ( Press 'Q' to break ) ----' thì gửi 'q' cho đến khi không còn thông báo này
    while '---- More ( Press \'Q\' to break ) ----' in output:
        channel.send(' ')
        await asyncio.sleep(0.5)
        output = channel.recv(65535).decode().strip()
        final_output += output
    return final_output

async def ssh_bras_gpon_hw_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet, service_portnet, service_portgnms, service_portims):
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
        command = phan_loai_command(commands, card, port, onu, slid, vlanims, vlanmytv, vlannet, service_portnet, service_portgnms,service_portims)
        results = []
        # Chạy lần lượt từng command
        for cmd in command:
            print(cmd)
            result = await execute_command(channel, cmd)
            results.append(result)
        session.close()
        return HTTPException(status_code=200, detail= results)
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
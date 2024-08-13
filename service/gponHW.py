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
        return ["display ont autofind all",
                "quit",
                "y"
                ]
    elif commands == "view_info_onu":
        return [f"display ont inf 0 {card} {port} {onu}",
                "quit",
                "y"
                ]
    elif commands == "delete_port":
        return [
            "config",
            f"undo service-port port 0/{card}/{port} ont {onu}",
            "y",
            f"interface gpon 0/{card}",
            f"ont delete {port} {onu}"
            "quit",
            "quit",
            "quit",
            "y"
        ]
    elif commands == "create_dvnet":
        return [
                "config",
                f"interface gpon 0/{card}",
                f"ont add {port} {onu} password-auth \"{slid}\" always-on omci ont-lineprofile-id 300 ont-srvprofile-id 300 desc \"noname\"",
                "quit",
                f"service-port {service_portnet} vlan {vlannet} gpon 0/{card}/{port} ont {onu} gemport 1 multi-service user-vlan  11 tag-transform translate inbound traffic-table index 300 outbound traffic-table index 300",
                f"service-port {service_portgnms} vlan 4040 gpon 0/{card}/{port} ont {onu} gemport 5 multi-service user-vlan 4000 tag-transform translate inbound traffic-table index 300 outbound traffic-table index 300",
                "quit",
                "quit",
                "y"
        ]
    elif commands == "dv_ims":
        return ["config",
                f"service-port {service_portims} vlan {vlanims} gpon 0/{card}/{port} ont {onu} gemport 3 multi-service user-vlan 13 tag-transform translate inbound traffic-table index 300 outbound traffic-table index 300",
                "quit",
                "quit",
                "y"
        ]    
    elif commands == "check_mac":
        return [f"display  mac-address  port 0/{card}/{port} ont {onu}",
                "quit",
                "y"
                ]
    elif commands == "check_service":
        return [f"display  service-port port 0/{card}/{port} ont {onu}",
                "quit",
                "y"
                ]
    elif commands == "change_sync_password":
        return ["Config",
                "interface  gpon 0/0",
                f"ont  modify {port} {onu} password {slid}",
                "quit",
                "quit",
                "quit",
                "y"
        ]
    elif commands == "change_sync_password_list":
        return ["Config",
                "interface  gpon 0/0",
                f"ont  modify {port} {onu} password {slid}",
                "quit",
                "quit",
        ]
    elif commands == "check_service_port":
        return [
            f"display service-port port 0/{card}/{port} ont {onu}",
            "quit",
            "y"
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
    
  # Kiểm tra nếu kết quả trả về chứa '---- More ( Press \'Q\' to break ) ----'
    if '---- More ( Press \'Q\' to break ) ----' in output:
        channel.send(' ')
        await asyncio.sleep(0.5)
        output = channel.recv(65535).decode().strip()
        final_output += output

        channel.send('q')
        await asyncio.sleep(0.5)
        output = channel.recv(65535).decode().strip()
        final_output += output

    channel.send('quit\n')
    await asyncio.sleep(0.5)
    output = channel.recv(65535).decode().strip()
    final_output += output

    channel.send('y\n')
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


async def execute_command_list(channel, cmd):
    channel.send(cmd + '\n')
    await asyncio.sleep(1)
    output = channel.recv(65535).decode().strip()
    final_output = output

    # Kiểm tra nếu kết quả trả về chứa '{ <cr>||<K> }' thì gửi thêm một lần enter
    if '{ <cr>||<K> }' in output or '{ <cr>|gemport<K> }:' in output or '{ <cr>|desc<K>|fiber-route<K>|ont-type<K> }:' in output or '{ <cr>|globalleave<K>|igmp-ipv6-version<K>|log<K>|max-bandwidth<K>|max-program<K>|quickleave<K>|video<K> }' or '{ <cr>|dedicated-net-id<K> }' in output:
        channel.send('\n')
        await asyncio.sleep(1)
        output = channel.recv(65535).decode().strip()
        final_output += output

  # Kiểm tra nếu kết quả trả về chứa '---- More ( Press \'Q\' to break ) ----'
    if '---- More ( Press \'Q\' to break ) ----' in output:
        channel.send(' ')
        await asyncio.sleep(0.5)
        output = channel.recv(65535).decode().strip()
        final_output += output

        channel.send('q')
        await asyncio.sleep(0.5)
        output = channel.recv(65535).decode().strip()
        final_output += output

    return final_output

async def control_gpon_hw(ipaddress, listconfig):
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
        
        results = []

        # Duyệt qua từng cấu hình trong listconfig
        for config in listconfig:
            commands = config["commands"]
            card = config["newcard"]
            port = config["newport"]
            onu = config["newonu"]
            slid = config["slid"]  # Lấy giá trị slid nếu có
            vlanims = config.get("vlanims", 0)
            vlanmytv = config.get("vlanmytv", 0)
            vlannet = config.get("vlannet", 0)
            print(vlanims)

            # Lấy các lệnh dựa trên loại lệnh
            command_list = phan_loai_command(commands, card, port, onu, slid, vlanims, vlanmytv, vlannet)
            
            # Thực hiện từng lệnh và lưu kết quả
            for cmd in command_list:
                result = await execute_command_list(channel, cmd)
                results.append(result)

        # Đóng phiên SSH
        channel.send('quit\n')
        channel.send('y\n')
        channel.close()
        session.close()

        # Trả về kết quả
        return HTTPException(status_code=200, detail=results)
    
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
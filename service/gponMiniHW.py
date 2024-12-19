import paramiko
import time
import os
import asyncio
from fastapi import HTTPException


# Lấy thông tin đăng nhập gpon
gpon_username = os.getenv("GPON_MINI_HW_USERNAME")
gpon_password = os.getenv("GPON_MINI_HW_PASSWORD")

print(gpon_username)
print(gpon_password)

def phan_loai_command(commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
    if commands == "sync_password":
        return ["display ont autofind all",
                "quit",
                #"y"
                ]
    elif commands == "view_info_onu":
        return [f"display ont info 0 {card} {port} {onu}",
                "quit",
                #"y"
                ]
    elif commands == "delete_port":
        return [
            "config",
            f"undo service-port port 0/{card}/{port} ont {onu}",
            #"y",
            f"interface gpon 0/{card}",
            f"ont delete {port} {onu}",
            "quit",
            "quit",
            "quit",
            #"y"
        ]
    elif commands == "create_dvnet":
        serviceport_gem1 = port * 64 + onu
        serviceport_gem5 = port * 64 + onu + 1024
        return ["config",
                "interface gpon 0/1",
                f"ont add {port} {onu} password-auth {slid} always-on omci ont-lineprofile-id 300 ont-srvprofile-id 300",
                "quit",
                f"service-port {serviceport_gem1} vlan {vlannet} gpon 0/1/{port} ont {onu} gemport 1 multi-service user-vlan 11 tag-transform translate inbound traffic-table name Fiber300M outbound traffic-table name Fiber300M",
                f"service-port {serviceport_gem5} vlan 4040 gpon 0/1/{port} ont {onu} gemport 5 multi-service user-vlan 4000 tag-transform translate inbound traffic-table name TR069 outbound traffic-table name TR069",
                "quit",
                "quit",
                #"y"
        ]
    elif commands == "dv_ims":
        serviceport_ims = port * 64 + onu + 512
        return [
                "config",
                f"service-port {serviceport_ims} vlan {vlanims} gpon 0/1/{port} ont {onu} gemport 3 multi-service user-vlan 13 tag-transform translate inbound traffic-table name VOIP outbound traffic-table name VOIP",
                "quit",
                "quit",
                #"y"
        ]
    elif commands == "dv_mytv":
        serviceport = port * 64 + onu + 1536
        return [
                "config",
               f"service-port {serviceport} vlan {vlanmytv} gpon 0/1/{port} ont {onu} gemport 2 multi-service user-vlan 12 tag-transform translate inbound traffic-table name IPTV outbound traffic-table name IPTV",
                f"btv",
                f"igmp user add service-port {serviceport} no-auth igmp-version v2",
                "quit",
                f"multicast-vlan 99",
                f"igmp multicast-vlan member service-port {serviceport}",
                "quit",
                "quit",
                #"y"
        ]   
    elif commands == "check_mac":
        return [f"display  mac-address  port 0/{card}/{port} ont {onu}",
                "quit",
                #"y"
                ]
    elif commands == "check_service":
        return [f"display  service-port port 0/{card}/{port} ont {onu}",
                "quit",
                #"y"
                ]
    elif commands == "change_sync_password":
        return ["Config",
                f"interface  gpon 0/{card}",
                f"ont  modify {port} {onu} password {slid}",
                "quit",
                "quit",
                "quit",
                #"y"
        ]
    elif commands == "change_sync_password_list":
        return [
                f"ont  modify {port} {onu} password {slid}"
        ]
    elif commands == "check_service_port":
        return [
            f"display service-port port 0/{card}/{port} ont {onu}",
            "quit",
            #"y"
        ]
    elif commands == "create_dvnet_list":
        serviceport_gem1 = port * 64 + onu
        serviceport_gem5 = port * 64 + onu + 1024
        return ["config",
                "interface gpon 0/1",
                f"ont add {port} {onu} password-auth {slid} always-on omci ont-lineprofile-id 300 ont-srvprofile-id 300",
                "quit",
                f"service-port {serviceport_gem1} vlan {vlannet} gpon 0/1/{port} ont {onu} gemport 1 multi-service user-vlan 11 tag-transform translate inbound traffic-table name Fiber300M outbound traffic-table name Fiber300M",
                f"service-port {serviceport_gem5} vlan 4040 gpon 0/1/{port} ont {onu} gemport 5 multi-service user-vlan 4000 tag-transform translate inbound traffic-table name TR069 outbound traffic-table name TR069",
                "quit"
        ]
    elif commands == "dv_ims_list":
        serviceport_ims = port * 64 + onu + 512
        return [
                "config",
                f"service-port {serviceport_ims} vlan {vlanims} gpon 0/1/{port} ont {onu} gemport 3 multi-service user-vlan 13 tag-transform translate inbound traffic-table name VOIP outbound traffic-table name VOIP",
                "quit"
        ]
    else:
        raise HTTPException(status_code=400, detail={"error": "Chức năng trên thiết bị này chưa được cập nhật"})
    

async def execute_command(channel, cmd):
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
  # Kiểm tra nếu có yêu cầu xác nhận khi thoát
    if "Check whether system data has been changed. Please save data before logout. Are you sure to log out? (y/n)[n]:" in output or "Are you sure to release service virtual port(s)? (y/n)[n]:" in output:
        channel.send('y\n')
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

        channel.send('quit')
        channel.send('\n')
        await asyncio.sleep(0.5)
        output = channel.recv(65535).decode().strip()
        final_output += output

        channel.send('y')
        channel.send('\n')
        await asyncio.sleep(0.5)
        output = channel.recv(65535).decode().strip()
        final_output += output

    return final_output

async def ssh_bras_gpon_minihw_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
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
        channel.close()
        session.close()
        return HTTPException(status_code=200, detail= results)
        
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
    
  # Kiểm tra nếu có yêu cầu xác nhận khi thoát
    if "Check whether system data has been changed. Please save data before logout. Are you sure to log out? (y/n)[n]:" in output:
        channel.send('y\n')
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

#Hàm điều khiển gpon mini hw tạo dãy
async def control_gpon_minihw_list(ipaddress, listconfig):
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
        channel.send('Config\n')
        await asyncio.sleep(0.5)
        channel.send('interface  gpon 0/1\n')
        await asyncio.sleep(0.5)
        output = channel.recv(65535).decode().strip()
        results.append(output)
        # Duyệt qua từng cấu hình trong listconfig
        for config in listconfig:
            # Chuyển đổi chuỗi lệnh thành danh sách
            command_list = config["commands"]
            card = config["newcard"]
            port = config["newport"]
            onu = config["newonu"]
            slid = config["slid"]  # Lấy giá trị slid nếu có
            vlanims = config["vlanims"]
            vlanmytv = config["vlanmytv"]
            vlannet = config["vlannet"]

            print(command_list)

            # Thực hiện từng lệnh
            for command in command_list:
                command_steps = phan_loai_command(command, card, port, onu, slid, vlanims, vlanmytv, vlannet)
                for step in command_steps:
                    result = await execute_command(channel, step)
                    print(result)
                    results.append(result)

        # Đóng phiên SSH
        channel.send('quit\n')
        await asyncio.sleep(0.5)
        channel.send('quit\n')
        await asyncio.sleep(0.5)
        channel.send('quit\n')
        await asyncio.sleep(0.5)
        channel.send('y\n')
        await asyncio.sleep(0.5)
        output = channel.recv(65535).decode().strip()  
        results.append(output)     
        channel.close()
        session.close()

        # Trả về kết quả
        return HTTPException(status_code=200, detail=results)
    
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
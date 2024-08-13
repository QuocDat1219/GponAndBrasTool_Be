import paramiko
import time
import asyncio
import os
import re
from fastapi import HTTPException

# Lấy thông tin đăng nhập gpon
gpon_username = os.getenv("GPON_ALU_USERNAME")
gpon_password = os.getenv("GPON_ALU_PASSWORD")

def phan_loai_command(commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
    if commands == "sync_password":
        return ["show pon unprovision-onu",
                "exit all",
                ]
    elif commands == "delete_port":
        return [
            f"configure equipment ont interface 1/1/{card}/{port}/{onu} admin-state down",
            "exit all",
            f"configure equipment ont no interface 1/1/{card}/{port}/{onu}",
            "exit all",
            "logout"
        ]
    elif commands == "create_dvnet":
        return [
            f"configure equipment ont interface 1/1/{card}/{port}/{onu} sw-ver-pland disabled subslocid {slid} fec-up disable sw-dnload-version disabled plnd-var SIP enable-aes enable sn-bundle-ctrl bundle",
            "exit all",
            f"configure equipment ont slot 1/1/{card}/{port}/{onu}/14 planned-card-type veip plndnumdataports 1 plndnumvoiceports 0 port-type uni admin-state up",
            "exit all",
            f"configure interface port uni:1/1/{card}/{port}/{onu}/14/1 admin-up",
            "exit all",
            f"configure bridge port 1/1/{card}/{port}/{onu}/14/1 max-unicast-mac 20",
            "exit all",
            f"configure qos interface  1/1/{card}/{port}/{onu}/14/1 upstream-queue 0 bandwidth-profile name:Fiber300M",
            "exit all",
            f"configure qos interface  1/1/{card}/{port}/{onu}/14/1 queue 0 shaper-profile name:Fiber300M",
            "exit all",
            f"configure bridge port  1/1/{card}/{port}/{onu}/14/1 vlan-id 11 tag single-tagged l2fwder-vlan {vlannet} vlan-scope local",
            "exit all",
            f"configure bridge port 1/1/{card}/{port}/{onu}/14/1 vlan-id 4000 tag single-tagged network-vlan 4040 vlan-scope local",
            "exit all",
            "logout"
        ]
    elif commands == "dv_mytv":
        return [
            f"configure qos interface 1/1/{card}/{port}/{onu}/14/1 upstream-queue 4 bandwidth-profile name:IPTV_up",
            "exit all",
            f"configure qos interface 1/1/{card}/{port}/{onu}/14/1 queue 4 shaper-profile name:IPTV_down_12M",
            "exit all",
            f"configure bridge port 1/1/{card}/{port}/{onu}/14/1 vlan-id 12 tag single-tagged network-vlan {vlanmytv} vlan-scope local",
            "exit all",
            f"configure bridge port 1/1/{card}/{port}/{onu}/14/1 vlan-id 12 max-unicast-mac 20",
            "exit all",
            f"configure igmp channel vlan:1/1/{card}/{port}/{onu}/14/1:12 max-num-group 254",
            "exit all",
            f"configure igmp channel vlan:1/1/{card}/{port}/{onu}/14/1:12 mcast-vlan-id 99",
            "exit all",
            "logout"
        ]
    elif commands == "dv_ims":
        return [
            f"configure qos interface 1/1/{card}/{port}/{onu}/14/1 queue 5 shaper-profile name:VoIP",
            f"configure qos interface 1/1/{card}/{port}/{onu}/14/1 upstream-queue 5 bandwidth-profile name:VoIP",
            f"configure bridge port 1/1/{card}/{port}/{onu}/14/1 vlan-id 13 tag single-tagged l2fwder-vlan {vlanims} vlan-scope local",
            f"configure bridge port 1/1/{card}/{port}/{onu}/14/1 vlan-id 4000 tag single-tagged l2fwder-vlan 4040 vlan-scope local",
            "exit all",
            "logout"
        ]
    elif commands == "status_port":
        return [f"show interface port ont:1/1/{card}/{port}/{onu}",
                "exit all",
                "logout"
                ]
    elif commands == "check_capacity":
        return [f"show equipment ont optics 1/1/{card}/{port}/{onu}",
                "exit all",
                "logout"
                ]
    elif commands == "check_mac":
        return [f"show vlan bridge-port-fdb 1/1/{card}/{port}/{onu}/14/1",
                "exit all",
                "logout"
                ]
    elif commands == "change_sync_password":
        return [f"configure equipment ont interface 1/1/{card}/{port}/{onu}",
            f"configure equipment ont interface 1/1/{card}/{port}/{onu} admin-state  down",
            f"configure equipment ont interface 1/1/{card}/{port}/{onu} no sernum",
            f"configure equipment ont interface 1/1/{card}/{port}/{onu} subslocid {slid}",
            f"configure equipment ont interface 1/1/{card}/{port}/{onu} admin-state  up",
            "exit all",
            "logout"
        ]
    elif commands == "change_sync_password_list":
        return [f"configure equipment ont interface 1/1/{card}/{port}/{onu}",
            f"configure equipment ont interface 1/1/{card}/{port}/{onu} admin-state  down",
            f"configure equipment ont interface 1/1/{card}/{port}/{onu} no sernum",
            f"configure equipment ont interface 1/1/{card}/{port}/{onu} subslocid {slid}",
            f"configure equipment ont interface 1/1/{card}/{port}/{onu} admin-state  up",
            "exit all",
        ]
    else:
        raise HTTPException(status_code=400, detail="Lệnh trên thiết bị này chưa được cập nhật")

# Hàm thực thi các command cho sync_password
async def execute_command_for_syncPassword(channel, cmd, is_sync_password=False):
    channel.send(cmd + '\n')
    await asyncio.sleep(1)
    
    output = ''
    # Đợi đến khi có lệnh unprovision-onu count: xuất hiện và kết thúc bằng lệnh typ:isadmin># (chỉ thực hiện cho sync_password)
    while True:
        part = channel.recv(65535).decode().strip()
        output += part
        if is_sync_password and 'unprovision-onu count :' in part:
            break
        if 'typ:isadmin>#' in part:
            break
        await asyncio.sleep(0.5)
    
    # Loại bỏ các ký tự load
    if is_sync_password:
        loading_patterns = [
            r'\u001b\[1D\\', r'\u001b\[1D\|', r'\u001b\[1D/', r'\u001b\[1D-', 
            r'\u001b\[1D', r'\n-\b\b'
        ]
        for pattern in loading_patterns:
            output = re.sub(pattern, '', output)
        
        # Giữ lại các dòng chứa ký tự ASCII
        output_lines = output.split('\n')
        output = '\n'.join(line for line in output_lines if any(c.isprintable() and ord(c) < 128 for c in line))
        
        return output.strip()
    
    return output.strip()

# Hàm thực thi các command khác
async def execute_command(channel, cmd):
    channel.send(cmd + '\n')
    await asyncio.sleep(0.5)
    output = channel.recv(65535).decode().strip()
    return output

async def ssh_bras_gpon_alu_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
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
            if commands == "sync_password":
                result = await execute_command_for_syncPassword(channel, cmd, is_sync_password=True)
            else:
                result = await execute_command(channel, cmd)
            # Gán các kết quả trả về vào mảng
            results.append(result)
        return HTTPException(status_code=200, detail=results)
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
    
    
async def control_gpon_alu(ipaddress, listconfig):
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
                result = await execute_command(channel, cmd)
                print(result)
                results.append(result)

        # Đóng phiên SSH
        channel.send('logout\n')
        channel.close()
        session.close()

        # Trả về kết quả
        return HTTPException(status_code=200, detail=results)
    
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")


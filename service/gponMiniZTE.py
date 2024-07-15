import asyncio
import os
import paramiko
import re
from fastapi import HTTPException

# Lấy thông tin đăng nhập gpon
gpon_username = os.getenv("MINIZTE_USERNAME")
gpon_password = os.getenv("MINIZTE_PASSWORD")

def phan_loai_command(commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
    if commands == "sync_password":
        return [
            "show pon onu un"
        ]
    elif commands == "delete_port":
        return [
            "configure t",
            f"interface gpon_olt-1/3/{port}",
            f"no onu {onu}"
        ]
    elif commands == "create_dvnet":
        return [
            "configure t",
            f"interface gpon_olt-1/3/{port}",
            f"onu {onu} type GW040 pw {slid}",
            "exit",
            f"interface gpon_onu-1/3/{port}:{onu}",
            "vport-mode manual",
            "tcont 1 name HSI profile T4_300M",
            "gemport 1 name HSI tcont 1",
            "vport 1 map-type vlan",
            "vport-map 1 1 vlan 11",
            "tcont 6 name GNMS profile Fiber300M",
            "gemport 6 name GNMS tcont 6",
            "vport 1 map-type vlan",
            "vport-map 1 6 vlan 4000",
            "exit",
            f"interface vport-1/3/{port}.{onu}:1",
            f"service-port 1 user-vlan 11 vlan {vlannet}",
            f"service-port 1 user-vlan 11 vlan {vlannet} egress Fiber300M",
            "service-port 6 user-vlan 4000 vlan 4040 egress Fiber300M",
            "exit",
            f"pon-onu-mng gpon_onu-1/3/{port}:{onu}",
            "service 1 gemport 1 vlan 11",
            "wan 1 service internet host 1",
            "wan-ip ipv4 mode pppoe vlan-profile HSI host 1",
            "service 6 gemport 6 vlan 4000",
            "exit"
        ]
    elif commands == "dv_mytv":
        return [
            "configure t",
            f"interface gpon_onu-1/3/{port}:{onu}",
            "vport-mode manual",
            "tcont 2 name IPTV profile T2_512K",
            "gemport 2 name IPTV tcont 2",
            "vport 1 map-type vlan",
            "vport-map 1 2 vlan 12",
            "exit",
            f"interface vport-1/3/{port}.{onu}:1",
            f"service-port 2 user-vlan 12 vlan {vlanmytv}",
            f"service-port 2 user-vlan 12 vlan {vlanmytv} egress HD",
            "exit",
            f"pon-onu-mng gpon_onu-1/3/{port}:{onu}",
            "service 2 gemport 2 vlan 12",
            "mvlan 12",
            "exit",
            "igmp mvlan 99",
            f"receive-port vport-1/3/{port}.{onu}:1"
        ]
    elif commands == "dv_ims":
        return [
            "configure t",
            f"interface gpon_onu-1/3/{port}:{onu}",
            "vport-mode manual",
            "tcont 3 name VOIP profile T1_80K",
            "gemport 3 name VOIP tcont 3",
            "vport 1 map-type vlan",
            "vport-map 1 3 vlan 13",
            "exit",
            f"interface vport-1/3/{port}.{onu}:1",
            f"service-port 3 user-vlan 13 vlan {vlanims}",
            f"service-port 3 user-vlan 13 vlan {vlanims} egress G_80K",
            "exit",
            f"pon-onu-mng gpon_onu-1/3/{port}:{onu}",
            "service 3 gemport 3 vlan 13",
            "voip protocol sip"
        ]
    elif commands == "check_capacity":
        return [f"show pon power attenuation gpon_onu-1/3/{port}:{onu}"]
    elif commands == "check_mac":
        return [f"show mac interface gpon_onu-1/3/{port}:{onu}"]
    elif commands == "change_sync_password":
        return ["configure terminal",
            f"interface  gpon_onu-1/3/{port}:{onu}",
            "sn-bind disable",
            f"auth-id pw {slid}",
            "end"
        ]
    else:
        raise HTTPException(status_code=400, detail="Lệnh trên thiết bị này chưa được cập nhật")

def clean_output(output):
    # Loại bỏ các ký tự điều khiển không mong muốn và xử lý backspace
    cleaned_output = re.sub(r'\x08+', '', output)  # Loại bỏ các ký tự backspace (\b)
    cleaned_lines = []
    for line in cleaned_output.splitlines():
        cleaned_lines.append(re.sub(r'\s+', ' ', line.strip()))  # Thay thế các khoảng trắng liên tiếp bằng 1 khoảng trắng
    return '\n'.join(cleaned_lines)

# Hàm thực thi các command khác
async def execute_command(channel, cmd):
    channel.send(cmd + '\n')
    await asyncio.sleep(0.5)
    output = channel.recv(65535).decode('latin-1').strip()
    final_ouput = clean_output(output)
    return final_ouput

async def ssh_bras_gpon_mini_zte_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
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
            result = await execute_command(channel, cmd)
            # Gán các kết quả trả về vào mảng
            results.append(result)
        return HTTPException(status_code=200, detail=results)
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

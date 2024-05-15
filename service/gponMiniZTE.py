import paramiko
import time
import os
import asyncio
from fastapi import HTTPException

# Lấy thông tin đăng nhập gpon
gpon_username = os.getenv("MINIZTE_USERNAME")
gpon_password = os.getenv("MINIZTE_PASSWORD")

print(gpon_username)
print(gpon_password)

def phan_loai_command(commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
        if commands == "sync_password":
            return ["show pon onu un"]
        elif commands == "delete_port":
            return [
                "configure t",
                f"interface gpon_olt-1/3/{port}",
                f"no onu {port}"
            ]
        elif commands == "create_dvnet":
            return [
                "configure t",
                f"interface gpon_olt-1/3/{port}",
                f"onu {onu} type GW040 pw 0100000001",
                "exit",
                f"interface gpon_onu-1/3/{port}:{onu}",
                # "sn-bind disable",
                "vport-mode manual",
                "tcont 1 name HSI profile T4_300M",
                "gemport 1 name HSI tcont 1",
                "vport 1 map-type vlan",
                "vport-map 1 1 vlan 11",
                "exit",
                f"interface vport-1/3/{port}.{onu}:1",
                f"service-port 1 user-vlan 11 vlan {vlannet}",
                f"service-port 1 user-vlan 11 vlan  {vlannet} egress Fiber300M",
                "exit",
                f"pon-onu-mng gpon_onu-1/3/{port}:{onu}",
                "service 1 gemport 1 vlan 11",
                "wan 1 service internet host 1",
                "wan-ip ipv4 mode pppoe vlan-profile HSI host 1"
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
        else:
            raise HTTPException(status_code=400, detail="Lệnh trên thiết bị này chưa được cập nhật")

async def execute_command(channel, cmd):
    channel.send(cmd + '\n')
    await asyncio.sleep(0.5)
    output = channel.recv(65535).decode().strip()
    return output

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
            print(cmd)
            result = await execute_command(channel, cmd)
            results.append(result)
            return HTTPException(status_code=200, detail= results)
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
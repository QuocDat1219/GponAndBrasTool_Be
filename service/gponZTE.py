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
    if command == "sync_password":
        return ["show pon onu uncfg",
                "exit"]
    elif command == "delete_port":
        return [
            "configure t",
            f"interface gpon-olt_1/{card}/{port}",
            f"no onu {onu}",
            "exit",
            "exit",
            "exit"
        ]
    elif command == "create_dvnet":
        return [
            "configure t",
            f"interface gpon-olt_1/{card}/{port}",
            f"onu {onu} type iGate-GW040 pw {slid}",
            "exit",
            f"interface gpon-onu_1/{card}/{port}:{onu}",
            "sn-bind disable",
            "tcont 1 name HSI profile T4_100M",
            "gemport 1 name HSI tcont 1",
            "gemport 1 traffic-limit upstream D3000T3000 downstream D3000T3000",
            "gemport 5 tcont 1",
            "switchport mode hybrid vport 1",
            "switchport mode hybrid vport 5",
            f"service-port 1 vport 1 user-vlan 11  vlan {vlannet}",
            "service-port 5 vport 5 user-vlan 4000 vlan 4040",
            "port-identification format VNPT vport 1",
            "pppoe-intermediate-agent enable vport 1",
            "pppoe-intermediate-agent trust true replace vport 1",
            "exit",
            f"pon-onu-mng gpon-onu_1/{card}/{port}:{onu}",
            "service 1 gemport 1 vlan 11",
            "service 5 gemport 5 vlan 4000",
            "wan-ip 1 mode pppoe vlan-profile HSI_PPPOE host 1",
            "wan 1 service internet host 1",
            "end",
            "exit",
            "exit",
            "exit"
        ]
    elif command == "dv_mytv":
        return [
            "configure t",
            f"interface gpon-onu_1/{card}/{port}:{onu}",
            "tcont 2 name IPTV profile T2_512K",
            "gemport 2 name IPTV tcont 2",
            "gemport 2 traffic-limit upstream G_IPTV downstream G_HD",
            f"service-port 2 vport 2 user-vlan 12 vlan {vlanmytv}",
            "exit",
            f"igmp mvlan 99 receive-port gpon-onu_1/{card}/{port}:{onu} vport 2",
            f"pon-onu-mng gpon-onu_1/{card}/{port}:{onu}",
            "service 2 gemport 2 vlan 12",
            "vlan port eth_0/4 mode tag vlan 12",
            "vlan port wifi_0/2 mode tag vlan 12",
            "mvlan 12",
            "wan 2 ethuni 4 service other mvlan 12",
            "dhcp-ip ethuni eth_0/4 from-internet",
            "exit",
            "exit",
            "configure t",
            f"pon-onu-mng gpon-onu_1/{card}/{port}:{onu}",
            "vlan port eth_0/3 mode tag vlan 12",
            "dhcp-ip ethuni eth_0/3 from-internet",
            "exit",
            "exit",
            "exit"
        ]
    elif command == "dv_ims":
        return [
            "configure terminal",
            f"interface gpon-onu_1/{card}/{port}:{onu}",
            "sn-bind disable",
            "tcont 3 name VOIP profile T1_80K",
            "gemport 3 name VOIP tcont 3",
            "gemport 3 traffic-limit upstream VoIP_1M downstream VoIP_1M",
            f"service-port 3 vport 3 user-vlan 13 vlan {vlanims}",
            "dhcpv4-l2-relay-agent enable vport 3",
            "dhcpv4-l2-relay-agent trust true replace vport 3",
            "exit",
            f"pon-onu-mng gpon-onu_1/{card}/{port}:{onu}",
            "service 3 gemport 3 vlan 13",
            "exit",
            "exit",
            "exit"
        ]
    elif command == "check_capacity":
        return [f"show pon power attenuation gpon-onu_1/{card}/{port}:{onu}",
                "exit"
                ]
    elif command == "check_mac":
        return [f"show mac gpon  onu  gpon-onu_1/{card}/{port}:{onu}",
                "exit"
                ]
    elif command == "change_sync_password":
        return ["configure  terminal",
                f"interface  gpon-onu_1/{card}/{port}:{onu}",
                "sn-bind disable",
                f"registration-method pw {slid}",
                "end",
                "exit",
                "y"
                ]
    elif command == "change_sync_password_list":
        return ["configure terminal",
            f"interface  gpon-onu_1/{card}/{port}:{onu}",
            "sn-bind disable",
            f"registration-method pw {slid}",
            "end"
        ]
    elif command == "create_dvnet_list":
        return [
            "configure t",
            f"interface gpon-olt_1/{card}/{port}",
            f"onu {onu} type iGate-GW040 pw {slid}",
            "exit",
            f"interface gpon-onu_1/{card}/{port}:{onu}",
            "sn-bind disable",
            "tcont 1 name HSI profile T4_100M",
            "gemport 1 name HSI tcont 1",
            "gemport 1 traffic-limit upstream D3000T3000 downstream D3000T3000",
            "gemport 5 tcont 1",
            "switchport mode hybrid vport 1",
            "switchport mode hybrid vport 5",
            f"service-port 1 vport 1 user-vlan 11  vlan {vlannet}",
            "service-port 5 vport 5 user-vlan 4000 vlan 4040",
            "port-identification format VNPT vport 1",
            "pppoe-intermediate-agent enable vport 1",
            "pppoe-intermediate-agent trust true replace vport 1",
            "exit",
            f"pon-onu-mng gpon-onu_1/{card}/{port}:{onu}",
            "service 1 gemport 1 vlan 11",
            "service 5 gemport 5 vlan 4000",
            "wan-ip 1 mode pppoe vlan-profile HSI_PPPOE host 1",
            "wan 1 service internet host 1",
            "end",
            "exit",
            "exit"
        ]
    elif command == "dv_ims_list":
        return [
            "configure terminal",
            f"interface gpon-onu_1/{card}/{port}:{onu}",
            "sn-bind disable",
            "tcont 3 name VOIP profile T1_80K",
            "gemport 3 name VOIP tcont 3",
            "gemport 3 traffic-limit upstream VoIP_1M downstream VoIP_1M",
            f"service-port 3 vport 3 user-vlan 13 vlan {vlanims}",
            "dhcpv4-l2-relay-agent enable vport 3",
            "dhcpv4-l2-relay-agent trust true replace vport 3",
            "exit",
            f"pon-onu-mng gpon-onu_1/{card}/{port}:{onu}",
            "service 3 gemport 3 vlan 13",
            "exit",
            "exit"
        ]
    else:
        raise HTTPException(status_code=400, detail="Lệnh trên thiết bị này chưa được cập nhật")
    
async def execute_command(reader, writer, cmd):
    writer.write(cmd.encode('ascii') + b'\n')
    await writer.drain()
    await asyncio.sleep(0.7)
    output = await reader.read(65535)
    return cmd + '\n' + output.decode('latin-1').strip()

async def ssh_bras_gpon_zte_command(ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
    try:
        reader, writer = await asyncio.open_connection(ipaddress, 23)

        # Xác thực với tên người dùng và mật khẩu
        writer.write(gpon_username.encode('ascii') + b'\n')
        await writer.drain()
        await asyncio.sleep(1)
        writer.write(gpon_password.encode('ascii') + b'\n')
        await writer.drain()
        await asyncio.sleep(1)

        # Thực thi các lệnh
        results = []
        for cmd in phan_loai_command(commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
            print(cmd)
            result = await execute_command(reader, writer, cmd)
            results.append(result)
        
        writer.close()
        return HTTPException(status_code=200, detail=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

# Hàm thực thi lệnh Telnet và trả về kết quả
async def execute_telnet_command(reader, writer, cmd):
    writer.write(cmd.encode('ascii') + b'\n')
    await writer.drain()
    await asyncio.sleep(0.7)
    output = await reader.read(65535)
    return cmd + '\n' + output.decode('latin-1').strip()

#Hàm điều khiển gpon zte tạo dãy
async def control_gpon_zte_list(ipaddress, listconfig):
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
            command_list = config["commands"]
            card = config["newcard"]
            port = config["newport"]
            onu = config["newonu"]
            slid = config["slid"]
            vlanims = config["vlanims"]
            vlanmytv = config["vlanmytv"]
            vlannet = config["vlannet"]

            # Phân loại và thực thi lệnh
            for command in command_list:
                command_steps = phan_loai_command(command, card, port, onu, slid, vlanims, vlanmytv, vlannet)
                for cmd in command_steps:
                    result = await execute_telnet_command(reader, writer, cmd)
                    print(result)
                    results.append(result)

        writer.write(b'exit\n')
        await writer.drain()
        await asyncio.sleep(0.7)
        writer.write(b'y\n')
        await writer.drain()
        await asyncio.sleep(0.7)
        writer.close()
        return HTTPException(status_code=200, detail=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

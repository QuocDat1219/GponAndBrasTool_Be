import paramiko
import time
from fastapi import HTTPException

def phan_loai_command(command, thongso1, thongso2, thongso3):
    if command == "sync_password":
        return ["show pon onu uncfg"]
    elif command == "delete_port":
        return [
            "configure t",
            f"interface gpon-olt_1/{thongso1}/{thongso2}/{thongso3}",
            "no onu 1"
        ]
    elif command == "create_dvnet":
        return [
            "configure t",
            "interface gpon-olt_1/1/1",
            "onu 1 type iGate-GW040 pw 0100000001",
            "exit",
            "interface gpon-onu_1/1/1:1",
            "tcont 1 name HSI profile T4_100M",
            "gemport 1 name HSI tcont 1",
            "gemport 1 traffic-limit upstream D3000T3000 downstream D3000T3000",
            "gemport 5 tcont 1",
            "switchport mode hybrid vport 1",
            "switchport mode hybrid vport 5",
            "service-port 1 vport 1 user-vlan 11  vlan 403",
            "service-port 5 vport 5 user-vlan 4000 vlan 4040",
            "port-identification format VNPT vport 1",
            "pppoe-intermediate-agent enable vport 1",
            "pppoe-intermediate-agent trust true replace vport 1",
            "exit",
            "pon-onu-mng gpon-onu_1/1/1:1",
            "service 1 gemport 1 vlan 11",
            "service 5 gemport 5 vlan 4000",
            "wan-ip 1 mode pppoe vlan-profile HSI_PPPOE host 1",
            "wan 1 service internet host 1",
            "end"
        ]
    elif command == "dv_mytv":
        return [
            "configure t",
            "interface gpon-onu_1/1/1:1",
            "tcont 2 name IPTV profile T2_512K",
            "gemport 2 name IPTV tcont 2",
            "gemport 2 traffic-limit upstream G_IPTV downstream G_HD",
            "service-port 2 vport 2 user-vlan 12 vlan 2409",
            "exit",
            "igmp mvlan 99 receive-port gpon-onu_1/1/1:1 vport 2",
            "pon-onu-mng gpon-onu_1/1/1:11",
            "service 2 gemport 2 vlan 12",
            "vlan port eth_0/4 mode tag vlan 12",
            "vlan port wifi_0/2 mode tag vlan 12",
            "mvlan 12",
            "wan 2 ethuni 4 service other mvlan 12",
            "dhcp-ip ethuni eth_0/4 from-internet",
            "exit",
            "exit",
            "configure t",
            "pon-onu-mng gpon-onu_1/1/1:1",
            "vlan port eth_0/3 mode tag vlan 12",
            "dhcp-ip ethuni eth_0/3 from-internet"
        ]
    elif command == "dv_ims":
        return [
            "configure terminal",
            "interface gpon-onu_1/1/1:1",
            "sn-bind disable",
            "tcont 3 name VOIP profile T1_80K",
            "gemport 3 name VOIP tcont 3",
            "gemport 3 traffic-limit upstream VoIP_1M downstream VoIP_1M",
            "service-port 3 vport 3 user-vlan 13 vlan 1500",
            "dhcpv4-l2-relay-agent enable vport 3",
            "dhcpv4-l2-relay-agent trust true replace vport 3",
            "exit",
            "pon-onu-mng gpon-onu_1/1/1:1",
            "service 3 gemport 3 vlan 13"
        ]
    elif command == "check_capacity":
        return ["show pon power attenuation gpon-onu_1/1/1:1"]
    elif command == "check_mac":
        return ["show mac gpon  onu  gpon-onu_1/1/1:1"]
    else:
        raise HTTPException(status_code=400, detail="Lệnh trên thiết bị này chưa được cập nhật")

def ssh_bras_gpon_zte_command(commands, thongso1, thongso2, thongso3):
    try:
        command = phan_loai_command(commands, thongso1, thongso2, thongso3)
        for cmd in command:
            print(cmd)
            time.sleep(1)  # Chờ một lát cho kết quả phản hồi
        raise HTTPException(status_code=200, detail="success")
    except HTTPException as http_error:
        raise http_error  # Ném lại HTTPException để FastAPI xử lý
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

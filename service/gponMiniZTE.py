import paramiko
import time
from fastapi import HTTPException

def phan_loai_command(command, thongso1, thongso2, thongso3):
        if command == "sync_password":
            return ["show pon onu un"]
        elif command == "delete_port":
            return [
                "configure t",
                f"interface gpon_olt-1/3/1",
                f"no onu 1"
            ]
        elif command == "create_dvnet":
            return [
                "configure t",
                f"interface gpon_olt-1/3/1",
                f"onu 1 type GW040 pw 0100000001",
                "exit",
                f"interface gpon_onu-1/3/1:1",
                "vport-mode manual",
                "tcont 1 name HSI profile T4_300M",
                "gemport 1 name HSI tcont 1",
                "vport 1 map-type vlan",
                "vport-map 1 1 vlan 11",
                "exit",
                f"interface vport-1/3/1.1:1",
                "service-port 1 user-vlan 11 vlan 901",
                f"service-port 1 user-vlan 11 vlan  901 egress Fiber300M",
                "exit",
                f"pon-onu-mng gpon_onu-1/3/1:1",
                "service 1 gemport 1 vlan 11",
                "wan 1 service internet host 1",
                "wan-ip ipv4 mode pppoe vlan-profile HSI host 1"
            ]
        elif command == "dv_mytv":
            return [
                "configure t",
                f"interface gpon_onu-1/3/1:1",
                "vport-mode manual",
                "tcont 2 name IPTV profile T2_512K",
                "gemport 2 name IPTV tcont 2",
                "vport 1 map-type vlan",
                "vport-map 1 2 vlan 12",
                "exit",
                f"interface vport-1/3/1.1:1",
                f"service-port 2 user-vlan 12 vlan 2401",
                f"service-port 2 user-vlan 12 vlan 2401 egress HD",
                "exit",
                f"pon-onu-mng gpon_onu-1/3/1:1",
                "service 2 gemport 2 vlan 12",
                "mvlan 12",
                "exit",
                "igmp mvlan 99",
                f"receive-port vport-1/3/1.1:1"
            ]
        elif command == "dv_ims":
            return [
                "configure t",
                f"interface gpon_onu-1/3/1:1",
                "vport-mode manual",
                "tcont 3 name VOIP profile T1_80K",
                "gemport 3 name VOIP tcont 3",
                "vport 1 map-type vlan",
                "vport-map 1 3 vlan 13",
                "exit",
                f"interface vport-1/3/1.1:1",
                f"service-port 3 user-vlan 13 vlan 1507",
                f"service-port 3 user-vlan 13 vlan 1507 egress G_80K",
                "exit",
                f"pon-onu-mng gpon_onu-1/3/1:1",
                "service 3 gemport 3 vlan 13",
                "voip protocol sip"
            ]
        elif command == "check_capacity":
            return [f"show pon power attenuation gpon_onu-1/3/1:1"]
        elif command == "check_mac":
            return [f"show mac interface gpon_onu-1/3/1:1"]
        else:
            raise HTTPException(status_code=400, detail="Lệnh trên thiết bị này chưa được cập nhật")
def ssh_bras_gpon_mini_zte_command(commands, thongso1, thongso2, thongso3):
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
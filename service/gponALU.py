import paramiko
import time
from fastapi import HTTPException
    
def phan_loai_command(command, thongso1, thongso2, thongso3):
        if command == "sync_password":
            return ["show pon unprovision-onu"]
        elif command == "delete_port":
            return [
                "configure equipment ont interface 1/1/1/1/1 admin-state down",
                "exit all",
                "configure equipment ont no interface 1/1/1/1/1",
                "exit all"
            ]
        elif command == "create_dvnet":
            return [
                "configure equipment ont interface 1/1/1/1/1 sw-ver-pland disabled subslocid 0100000001 fec-up disable sw-dnload-version disabled plnd-var SIP enable-aes enable sn-bundle-ctrl bundle",
                "exit all",
                "configure equipment ont slot 1/1/1/1/1/14 planned-card-type veip plndnumdataports 1 plndnumvoiceports 0 port-type uni admin-state up",
                "exit all",
                "configure interface port uni:1/1/1/1/1/14/1 admin-up",
                "exit all",
                "configure bridge port 1/1/1/1/1/14/1 max-unicast-mac 20",
                "exit all",
                "configure qos interface  1/1/1/1/1/14/1 upstream-queue 0 bandwidth-profile name:Fiber300M",
                "exit all",
                "configure qos interface  1/1/1/1/1/14/1 queue 0 shaper-profile name:Fiber300M",
                "exit all",
                "configure bridge port  1/1/1/1/1/14/1 vlan-id 11 tag single-tagged l2fwder-vlan 514 vlan-scope local",
                "exit all",
                "configure bridge port 1/1/1/1/1/14/1 vlan-id 4000 tag single-tagged network-vlan 4040 vlan-scope local",
                "exit all"
            ]
        elif command == "dv_mytv":
            return [
                "configure qos interface 1/1/1/1/1/14/1 upstream-queue 4 bandwidth-profile name:IPTV_up",
                "exit all",
                "configure qos interface 1/1/1/1/1/14/1 queue 4 shaper-profile name:IPTV_down_12M",
                "exit all",
                "configure bridge port 1/1/1/1/1/14/1 vlan-id 12 tag single-tagged network-vlan 2406 vlan-scope local",
                "exit all",
                "configure igmp channel vlan:1/1/1/1/1/14/1:12 max-num-group 254",
                "exit all",
                "configure igmp channel vlan:1/1/1/1/1/14/1:12 mcast-vlan-id 99",
                "exit all"
            ]
        elif command == "dv_ims":
            return [
                "configure qos interface 1/1/1/1/1/14/1 queue 5 shaper-profile name:VoIP",
                "exit all",
                "configure qos interface 1/1/1/1/1/14/1 upstream-queue 5 bandwidth-profile name:VoIP",
                "exit all",
                "configure bridge port 1/1/1/1/1/14/1 vlan-id 13 tag single-tagged l2fwder-vlan 1502 vlan-scope local",
                "exit all",
                "configure bridge port 1/1/1/1/1/14/1 vlan-id 4000 tag single-tagged l2fwder-vlan 4040 vlan-scope local",
                "exit all"
            ]
        elif command == "status_port":
            return ["show interface port ont:1/1/1/1/1"]
        elif command == "check_capacity":
            return ["show equipment ont optics 1/1/1/1/1"]
        elif command == "check_mac":
            return ["show vlan bridge-port-fdb 1/1/1/1/1/14/1"]
        else:
            raise HTTPException(status_code=400, detail="Lệnh trên thiết bị này chưa được cập nhật")

def ssh_bras_gpon_alu_command(commands, thongso1, thongso2, thongso3):
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
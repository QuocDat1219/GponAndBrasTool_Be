import paramiko
import time
import asyncio
import os
from fastapi import HTTPException


# Lấy thông tin đăng nhập gpon
gpon_username = os.getenv("GPON_ALU_USERNAME")
gpon_password = os.getenv("GPON_ALU_PASSWORD")
# gpon_ip = os.getenv("GPON_ALU_IP")

def phan_loai_command(commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
        if commands == "sync_password":
            return ["show pon unprovision-onu"]
        elif commands == "delete_port":
            return [
                f"configure equipment ont interface 1/1/{card}/{port}/{onu} admin-state down\n",
                f"configure equipment ont no interface 1/1/{card}/{port}/{onu}\n",
                "exit all"
            ]
        elif commands == "create_dvnet":
            return [
                f"configure equipment ont interface 1/1/{card}/{port}/{onu} sw-ver-pland disabled subslocid {slid} fec-up disable sw-dnload-version disabled plnd-var SIP enable-aes enable sn-bundle-ctrl bundle\n",

                f"configure equipment ont slot 1/1/{card}/{port}/{onu}/14 planned-card-type veip plndnumdataports 1 plndnumvoiceports 0 port-type uni admin-state up\n",

                f"configure interface port uni:1/1/{card}/{port}/{onu}/14/1 admin-up\n",

                f"configure bridge port 1/1/{card}/{port}/{onu}/14/1 max-unicast-mac 20\n",

                f"configure qos interface  1/1/{card}/{port}/{onu}/14/1 upstream-queue 0 bandwidth-profile name:Fiber300M\n",

                f"configure qos interface  1/1/{card}/{port}/{onu}/14/1 queue 0 shaper-profile name:Fiber300M\n",

                f"configure bridge port  1/1/{card}/{port}/{onu}/14/1 vlan-id 11 tag single-tagged l2fwder-vlan {vlannet} vlan-scope local\n",

                f"configure bridge port 1/1/{card}/{port}/{onu}/14/1 vlan-id 4000 tag single-tagged network-vlan 4040 vlan-scope local\n",
                f"exit all\n"
            ]
        elif commands == "dv_mytv":
            return [
                f"configure qos interface 1/1/{card}/{port}/{onu}/14/1 upstream-queue 4 bandwidth-profile name:IPTV_up\n",
                "exit all\n",
                f"configure qos interface 1/1/{card}/{port}/{onu}/14/1 queue 4 shaper-profile name:IPTV_down_12M\n",
                "exit all\n",
                f"configure bridge port 1/1/{card}/{port}/{onu}/14/1 vlan-id 12 tag single-tagged network-vlan {vlanmytv} vlan-scope local\n",
                "exit all\n",
                f"configure bridge port 1/1/{card}/{port}/{onu}/14/1 vlan-id 12 max-unicast-mac 20\n",
                "exit all\n",
                f"configure igmp channel vlan:1/1/{card}/{port}/{onu}/14/1:12 max-num-group 254\n",
                "exit all\n",
                f"configure igmp channel vlan:1/1/{card}/{port}/{onu}/14/1:12 mcast-vlan-id 99\n",
                "exit all\n"
            ]
        elif commands == "dv_ims":
            return [
                f"configure qos interface 1/1/{card}/{port}/{onu}/14/1 queue 5 shaper-profile name:VoIP\n",
                f"configure qos interface 1/1/{card}/{port}/{onu}/14/1 upstream-queue 5 bandwidth-profile name:VoIP\n",
                f"configure bridge port 1/1/{card}/{port}/{onu}/14/1 vlan-id 13 tag single-tagged l2fwder-vlan {vlanims} vlan-scope local\n",
                f"configure bridge port 1/1/{card}/{port}/{onu}/14/1 vlan-id 4000 tag single-tagged l2fwder-vlan 4040 vlan-scope local\n",
                "exit all\n"
            ]
        elif commands == "status_port":
            return [f"show interface port ont:1/1/{card}/{port}/{onu}\n"]
        elif commands == "check_capacity":
            return [f"show equipment ont optics 1/1/{card}/{port}/{onu}\n"]
        elif commands == "check_mac":
            return [f"show vlan bridge-port-fdb 1/1/{card}/{port}/{onu}/14/1\n"]
        else:
            raise HTTPException(status_code=400, detail="Lệnh trên thiết bị này chưa được cập nhật")

async def execute_command(channel, cmd):
    channel.send(cmd + '\n')
    await asyncio.sleep(1)
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
            print(cmd)
            result = await execute_command(channel, cmd)
            results.append(result)
        return HTTPException(status_code=200, detail= results)
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")


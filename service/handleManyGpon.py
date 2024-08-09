import asyncio
from fastapi import HTTPException

from service.gponALU import ssh_bras_gpon_alu_command
from service.gponHW import ssh_bras_gpon_hw_command
from service.gponMiniHW import ssh_bras_gpon_minihw_command
from service.gponZTE import ssh_bras_gpon_zte_command
from service.gponMiniZTE import ssh_bras_gpon_mini_zte_command

async def controlManygpon(loai_thiet_bi, ipaddress, commands, card, port, onu, slid, vlanims, vlanmytv, vlannet):
    try:
        command_list = commands.strip('[]').split(',')
        command_list = [cmd.strip().strip('"') for cmd in command_list]
        
        results = {}
        for command in command_list:
            print (command)
            if loai_thiet_bi == "GPON ALU":
                result = await ssh_bras_gpon_alu_command(ipaddress, command, card, port, onu, slid, vlanims, vlanmytv, vlannet)
            elif loai_thiet_bi == "GPON HW":
                result = await ssh_bras_gpon_hw_command(ipaddress, command, card, port, onu, slid, vlanims, vlanmytv, vlannet)
            elif loai_thiet_bi == "GPON Mini HW":
                result = await ssh_bras_gpon_minihw_command(ipaddress, command, card, port, onu, slid, vlanims, vlanmytv, vlannet)
            elif loai_thiet_bi == "GPON ZTE":
                result = await ssh_bras_gpon_zte_command(ipaddress, command, card, port, onu, slid, vlanims, vlanmytv, vlannet)
            elif loai_thiet_bi == "GPON MINI ZTE":
                result = await ssh_bras_gpon_mini_zte_command(ipaddress, command, card, port, onu, slid, vlanims, vlanmytv, vlannet)
            else:
                raise HTTPException(status_code=400, detail="Thiết bị này không được hỗ trợ")
            results[command] = result
        return results
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

import paramiko
import time
from service.gponZTE import ssh_bras_gpon_zte_command
from service.gponMiniZTE import ssh_bras_gpon_mini_zte_command
from service.gponHW import ssh_bras_gpon_hw_command
from service.gponALU import ssh_bras_gpon_alu_command
from fastapi import HTTPException

def phan_loai_thiet_bi(commands, device_types, thongso1, thongso2, thongso3):
    if device_types == "GPON ZTE":
        ssh_bras_gpon_zte_command(commands, thongso1, thongso2, thongso3)
    elif device_types == "GPON MINI ZTE":
        ssh_bras_gpon_mini_zte_command(commands, thongso1, thongso2, thongso3)
    elif device_types == "GPON HW":
        ssh_bras_gpon_hw_command(commands, thongso1, thongso2, thongso3)
    elif device_types == "GPON ALU":
        ssh_bras_gpon_alu_command(commands, thongso1, thongso2, thongso3)
    else:
        ssh_bras_command(commands)
        
def phan_loai_commmand(commnad):
    if commnad == "check_authentication":
        return ["show subscribers mac-address 4c:12:e8:00:67:71"]
    elif commnad == "check_lock_mac":
        return ["show pppoe lockout | match 4c:12:e8:00:67:71"]
    elif commnad == "clear_bras":
        return ["clear pppoe lockout mac-address 4c:12:e8:00:67:71"]
    else:
        raise HTTPException(status_code=400, detail="Lệnh trên thiết bị này chưa được cập nhật")

def ssh_bras_command(commands):
    try:
        command = phan_loai_commmand(commands)
        for cmd in command:
            print(cmd)
            time.sleep(1)  # Chờ một lát cho kết quả phản hồi
        raise HTTPException(status_code=200, detail="success")
    except HTTPException as http_error:
        raise http_error  # Ném lại HTTPException để FastAPI xử lý
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

import paramiko
import time
from fastapi import HTTPException

def phan_loai_command(command,thongso1, thongso2, thongso3):
    if command == "sync_password":
        return ["display  ont autofind all"]
    elif command == "delete_port":
        return [
            "config",
            "undo service-port port 0/0/0 ont 59",
            "interface gpon 0/0",
            "ont delete  0  59"
        ]

def ssh_bras_gpon_hw_command(commands,thongso1, thongso2, thongso3):
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
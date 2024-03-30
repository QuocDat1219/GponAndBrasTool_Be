import paramiko
import time
import os
from fastapi import HTTPException


# Lấy thông tin đăng nhập bras
hostname_bras = os.getenv('HOSTNAME_BRAS')
hostname_bras_pre = os.getenv('HOSTNAME_BRAS_PRE')
user_bras = os.getenv('USER_BRAS')
password_bras = os.getenv('PASSWORD')


def phan_loai_command(command,card, port, onu, slid):
    if command == "sync_password":
        return ["display  ont autofind all"]
    elif command == "delete_port":
        return [
            "config",
            "undo service-port port 0/0/0 ont 59",
            "interface gpon 0/0",
            "ont delete  0  59"
        ]

def ssh_bras_gpon_hw_command(commands,card, port, onu, slid):
    try:
        session = paramiko.SSHClient()
        session.load_system_host_keys()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(hostname_bras_pre, username=user_bras, password=password_bras)
        
        command = phan_loai_command(commands,card, port, onu, slid)
        for cmd in command:
            print(cmd)
            stdin, stdout, stderr = session.exec_command(cmd)
            time.sleep(0.5)
            output = stdout.read().decode('utf-8').strip()
            print("output session: " + output)
            return output
    except HTTPException as http_error:
        raise http_error  # Ném lại HTTPException để FastAPI xử lý
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
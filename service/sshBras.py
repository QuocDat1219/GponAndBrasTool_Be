import paramiko
import os
import time
from fastapi import HTTPException 

# Lấy thông tin đăng nhập bras
hostname_bras = os.getenv('HOSTNAME_BRAS')
hostname_bras_pre = os.getenv('HOSTNAME_BRAS_PRE')
user_bras = os.getenv('USER_BRAS')
password_bras = os.getenv('PASSWORD')

def phan_loai_command(command, mac):
    if command == "check_auth_mac":
        return f'show subscribers mac-address {mac}'
    elif command == "check_lock_mac":
        return f'show pppoe lockout | match {mac}'
    elif command == 'clear_in_bras':
        return f'clear pppoe lockout mac-address {mac}'
     
def exploit_bras_vlg01(command, mac):
    try:
        # session = paramiko.SSHClient()
        # session.load_system_host_keys()
        # session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # session.connect(hostname_bras, username=user_bras, password=password_bras)
        
        cmd = phan_loai_command(command, mac)
        exit_cmd = f"exit"
        print(cmd)
        
        # stdin, stdout, stderr = session.exec_command(cmd)
        # time.sleep(0.5)
        # output = stdout.read().decode('utf-8').strip()
        
        # session.exec_command(exit_cmd)
        # time.sleep(0.5)
        # session.close()

        # return output
    except HTTPException as http_error:
        raise http_error  # Ném lại HTTPException để FastAPI xử lý
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

def exploit_bras_vlg02(command, mac):
    try:
        # session = paramiko.SSHClient()
        # session.load_system_host_keys()
        # session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # session.connect(hostname_bras_pre, username=user_bras, password=password_bras)
        
        cmd = phan_loai_command(command, mac)
        exit_cmd = f"exit"
        print(cmd)
        
        # stdin, stdout, stderr = session.exec_command(cmd)
        # time.sleep(0.5)
        # output = stdout.read().decode('utf-8').strip()
        
        # session.exec_command(exit_cmd)
        # time.sleep(0.5)
        # session.close()

        # return output
    except HTTPException as http_error:
        raise http_error  # Ném lại HTTPException để FastAPI xử lý
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
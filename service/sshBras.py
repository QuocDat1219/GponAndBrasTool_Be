import paramiko
import os
import time
from fastapi import HTTPException 

# Lấy thông tin đăng nhập bras
hostname_bras = os.getenv('HOSTNAME_BRAS')
user_bras = os.getenv('USER_BRAS')
password_bras = os.getenv('PASSWORD')

print(hostname_bras)
print(user_bras)
print(password_bras)

def phan_loai_command(command, mac):
    if command == "check_auth_mac":
        return f'sho_sub_mac {mac}\n'
    elif command == "check_lock_mac":
        return f'sho_pppoe_lockout {mac}\n'
    elif command == "clear_in_bras":
        return f'clear_lockout\n'
     
def ssh_bras_command(command, mac):
    try:
        session = paramiko.SSHClient()
        session.load_system_host_keys()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(hostname_bras, username=user_bras, password=password_bras)
        
        cmd = phan_loai_command(command, mac)
        exit_cmd = "exit\n"
        output = ''

        # Tạo kênh ssh bras
        ssh_channel = session.invoke_shell()
        ssh_channel.send(cmd)

        # Thực hiện đợi cho tới khi nhận được dấu nhắc lệnh ở dòng mới
        while not output.endswith('~$ '):
            output += ssh_channel.recv(1024).decode()
        print(output)

        output_lines = output.split('\n')
        
        # Gửi lệnh exit_cmd để thoát ra khỏi phiên SSH
        ssh_channel.send(exit_cmd)
        
        session.close()
        
        raise HTTPException(status_code=200, detail={"msg": "success", "data": output_lines})
    
    except HTTPException as http_error:
        raise http_error  # Ném lại HTTPException để FastAPI xử lý
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
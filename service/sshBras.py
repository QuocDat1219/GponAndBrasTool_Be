import paramiko
import os
import re
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

def clean_output(output):
    # Loại bỏ các ký tự điều khiển ANSI và những ký tự không mong muốn khác
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    cleaned_output = ansi_escape.sub('', output)
    # Thêm ký tự ngắt dòng cho mỗi dòng
    cleaned_output = cleaned_output.replace('\r', '').split('\n')
    cleaned_output = [line + '\r\n' for line in cleaned_output]
    return cleaned_output

def ssh_bras_command(command, mac):
    try:
        session = paramiko.SSHClient()
        session.load_system_host_keys()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(hostname_bras, username=user_bras, password=password_bras)
        
        if len(mac) < 17 or len(mac) > 17:
            raise HTTPException(status_code=500, detail=f"Địa chỉ mac không đúng định dạng")
        else:
            cmd = phan_loai_command(command, mac)
            exit_cmd = "exit\n"
            output = ''
            # Tạo kênh ssh bras
            ssh_channel = session.invoke_shell()
            ssh_channel.send(cmd)

        # Thực hiện đợi cho tới khi nhận được dấu nhắc lệnh ở dòng mới
        while not output.endswith('~$ '):
            output += ssh_channel.recv(1024).decode()
        
        # Làm sạch kết quả đầu ra và thêm ký tự ngắt dòng
        cleaned_output = clean_output(output)
        print(cleaned_output)

        # Gửi lệnh exit_cmd để thoát ra khỏi phiên SSH
        ssh_channel.send(exit_cmd)
        
        session.close()
        
        raise HTTPException(status_code=200, detail={"msg": "success", "data": cleaned_output})
    
    except HTTPException as http_error:
        raise http_error  # Ném lại HTTPException để FastAPI xử lý
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
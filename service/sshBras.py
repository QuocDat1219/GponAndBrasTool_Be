import paramiko
import os
import re
import asyncio
from fastapi import HTTPException

# Lấy thông tin đăng nhập bras
hostname_bras = os.getenv('HOSTNAME_BRAS')
user_bras = os.getenv('USER_BRAS')
password_bras = os.getenv('PASSWORD')

def commad_with_param(command, *args):
    # Xử lý các trường hợp còn lại
    if command == "check_auth_mac":
        return f'sho_sub_mac {args[0]}\n'
    elif command == "check_lock_mac":
        return f'sho_pppoe_lockout {args[0]}\n'
    elif command == "check_user_bras":
        return f'sho_sub_acc {args[0]}\n'
    elif command == "clear_user_bras":
        return f"clear_user {args[0]}\n"
    else:
        raise HTTPException(status_code=400, detail=f"Thiếu đối số trong lệnh") 

def command_no_param(command):
    if command == "clear_in_bras":
        return 'clear_lockout\n'
    else:
        raise HTTPException(status_code=400, detail=f"Command không hợp lệ")  

def clean_output(output):
    # Loại bỏ các ký tự điều khiển ANSI và những ký tự không mong muốn khác
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    unwanted_patterns = [
        r'Welcome to Ubuntu.*',
        r'\* Documentation:.*',
        r'\* Management:.*',
        r'\* Support:.*',
        r'Expanded Security Maintenance.*',
        r'\d+ updates can be applied immediately.*',
        r'To see these additional updates.*',
        r'\d+ additional security updates.*',
        r'Learn more about enabling ESM Apps.*',
        r'New release .+ available.*',
        r'Run .+ to upgrade to it.*',
        r'Your Hardware Enablement Stack.*',
        r'\*\*\* System restart required \*\*\*',
        r'Last login: .*'
    ]

    cleaned_output = ansi_escape.sub('', output)
    lines = cleaned_output.split('\n')
    cleaned_lines = [line for line in lines if not any(re.match(pattern, line) for pattern in unwanted_patterns)]
    
    # Thêm ký tự ngắt dòng cho mỗi dòng
    cleaned_lines = [line + '\n' for line in cleaned_lines if line.strip() != '']
    return cleaned_lines

async def ssh_bras_command_with_mac(command, mac):
    try:
        session = paramiko.SSHClient()
        session.load_system_host_keys()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(hostname_bras, username=user_bras, password=password_bras)
        if len(mac) < 17 or len(mac) > 17:
            raise HTTPException(status_code=500, detail=f"Địa chỉ mac không đúng định dạng")
        else:
            cmd = commad_with_param(command, mac)
            print(cmd)
            response = await execute_ssh_command(session, cmd)
            if response["status_code"] != 200:
                raise HTTPException(status_code=response["status_code"], detail=response["result"]["data"])
            return response["result"]
    
    except HTTPException as http_error:
        raise http_error  # Ném lại HTTPException để FastAPI xử lý
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")
    

async def execute_ssh_command(session, cmd):
    try:
        ssh_channel = session.invoke_shell()
        ssh_channel.send(cmd)
        await asyncio.sleep(0.5)
        
        output = ''
        while not output.endswith('~$ '):
            output += ssh_channel.recv(1024).decode()
            await asyncio.sleep(0.5)
        
        cleaned_output = clean_output(output)
        print(cleaned_output)
        
        ssh_channel.send("exit\n")
        session.close()
        
        return {"status_code": 200, "result": {"msg": "success", "data": cleaned_output}}
    
    except Exception as e:
        return {"status_code": 500, "result": {"msg": "error", "data": str(e)}}

async def ssh_bras_command_with_username(command, username_bras):
    try:
        session = paramiko.SSHClient()
        session.load_system_host_keys()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(hostname_bras, username=user_bras, password=password_bras)
        if len(username_bras) <= 0:
            raise HTTPException(status_code=400, detail="Chưa nhập username")
        else:
            cmd = commad_with_param(command, username_bras)
            print(cmd)
            response = await execute_ssh_command(session, cmd)
            if response["status_code"] != 200:
                raise HTTPException(status_code=response["status_code"], detail=response["result"]["data"])
            return response["result"]
    
    except HTTPException as http_error:
        raise http_error
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

async def ssh_bras_command(command):
    try:
        session = paramiko.SSHClient()
        session.load_system_host_keys()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(hostname_bras, username=user_bras, password=password_bras)
       
        cmd = command_no_param(command)
        print(cmd)
        # Gọi hàm thực thi command
        response = await execute_ssh_command(session, cmd)
        if response["status_code"] != 200:
            raise HTTPException(status_code=response["status_code"], detail=response["result"]["data"])
        return response["result"]
    
    except HTTPException as http_error:
        raise http_error  # Ném lại HTTPException để FastAPI xử lý
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"error: {str(e)}")

async def execute_ssh_command(session, cmd):
    try:
        ssh_channel = session.invoke_shell()
        ssh_channel.send(cmd)
        await asyncio.sleep(0.5)
        
        output = ''
        while not output.endswith('~$ '):
            output += ssh_channel.recv(1024).decode()
            await asyncio.sleep(0.5)
        
        cleaned_output = clean_output(output)
        print(cleaned_output)
        
        ssh_channel.send("exit\n")
        session.close()
        
        return {"status_code": 200, "result": {"msg": "success", "data": cleaned_output}}
    
    except Exception as e:
        return {"status_code": 500, "result": {"msg": "error", "data": str(e)}}
    
async def clear_user_bras(command, username_bras):
    if not command or not username_bras:
        raise HTTPException(status_code=400, detail="Thiếu command hoặc user trong request body")
    
    users_list = username_bras.strip('[]').split(',')
    results_data = []
    
    # Xử lý kết quả trả về sau mỗi lệnh và gộp vào 1 mảng
    for user in users_list:
        user = user.strip()
        result = await ssh_bras_command_with_username(command, user)
        print(result)
        if result["msg"] == "success":
            results_data.append(result["data"])
        else:
            raise HTTPException(status_code=500, detail=result["data"])
    
    return {"msg": "success", "data": results_data}
import paramiko
import time

def phan_loai_command(command):
    if command == f"sync_password":
        request = f'show pon onu un'
    elif command == f'delete_port':
        request = f"""
                configure t
                interface  gpon_olt-1/3/1
                no onu 1
            """
    return request

def ssh_bras_gpon_mini_zte_command(commands):
    try:
        # # Tạo kết nối SSH
        # session = paramiko.SSHClient()
        # session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # session.connect(ip_address, username=username, password=password)

        # # Tạo một kênh shell
        # shell = session.invoke_shell()

        # # Gửi lệnh tới thiết bị BRAS
        
        # shell.send(phan_loai_command(commands) + "\n")
        # time.sleep(1)  # Chờ một lát cho kết quả phản hồi

        # # Nhận kết quả từ thiết bị BRAS
        # output = shell.recv(65535).decode('utf-8')

        # # Đóng kết nối SSH
        # session.close()
        
        result = phan_loai_command(commands)
        print(result)
        return result
    except Exception as e:
        return str(e)
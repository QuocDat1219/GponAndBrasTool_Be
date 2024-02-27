import paramiko
import time

def ssh_bras_command(commands, ip_address, username, password):
    # print (commands,ip_address,username,password)

    try:
        {
        'global_delay_factor': 0.5,  # Tăng thời gian xác thực SSH
        'banner_timeout': 0.5,  # Đặt timeout cho banner
        'allow_agent': False,  # Tắt sử dụng SSH agent
        'use_keys': False,  # Tắt sử dụng SSH keys
        'alt_host_keys': False,  # Tắt sử dụng alternative host keys
        'fast_cli': True,  # Tăng tốc độ xử lý lệnh
        'global_cmd_verify': False
        }
        
        #Tạo kết nối sshClient từ paramiko
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #Kết nối đến brass
        session.connect(ip_address, username, password)
        #Tạo kênh ssh
        channel = session.invoke_shell()
        # Gửi từng lệnh SSH và cập nhật kết quả
        for command in commands:
            channel.send(command + "    \n")
            time.sleep(1)  # Thời gian chờ để nhận kết quả, có thể điều chỉnh tùy thuộc vào thiết bị và mạng                
            output = channel.recv(2048).decode('utf-8')# Nhận kết quả từ kênh SSH
            time.sleep(1)
            #print(output)                
            if "More" in output: # Kiểm tra xem có chữ "More" trong kết quả không                    
                channel.send("   ") # Gửi một dấu cách để tiếp tục hiển thị nội dung
                #time.sleep(1)  # Đợi một khoảng thời gian để nhận kết quả tiếp theo        
                # self.update_output(f"{output}\n") # Hiển thị kết quả trong ScrollText
                print(f"{output}\n")
    except Exception as e:
        error_message = f"SSH Connection to {ip_address} failed: {str(e)}"
        # self.update_output(f"\n{error_message}\n")
        print(f"{output}\n")

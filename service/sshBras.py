import paramiko
import time
from service.gponZTE import ssh_bras_gpon_zte_command
from service.gponMiniZTE import ssh_bras_gpon_mini_zte_command

def phan_loai_thiet_bi(commands, device_types):
    if device_types == f'GPON ZTE':
        ssh_bras_gpon_zte_command(commands)
    elif device_types == f'GPON MINI ZTE':
        ssh_bras_gpon_mini_zte_command(commands)
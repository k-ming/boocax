# -*- coding: utf-8 -*-
from socket import *

from case.lowPower import lowPower
from case.testCharge import testCharge
from comn.configRead import Read
from comn.pack2bytes import pack2bytes
from comn.receive2dic import RecvTread
import time

3  # ------------------------------------
4  # Name:         bukesi
5  # Description:  
6  # Author:       kingming
7  # Date:         2020/4/10
8  # ------------------------------------


# 读取配置文件
R = Read('conf/config.ini')
server_ip = R.getInfo('info', 'server_ip')

# 过滤消息
set_filter = {"message_type": "set_filter","filter": ["laser", "all_file_info", "report_sensor_data_info",   "set_sensor_data_info", "report_basic_status", 'sensor_power_status', 'report_stat',   'report_pos_vel_status', 'auto_guided_task_status', 'device_status', 'local_path', 'register_status', 'all_robot_info',   'sonar', 'config_signature']}

def subscribe():
    # Socket TCP
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_ip, 6789))
    # status
    json_packed = pack2bytes(R.getInfo('status', 'reg_client_message'))  # 注册客户端
    s.send(json_packed)
    json_packed = pack2bytes(set_filter)  # 过滤消息
    s.send(json_packed)
    # start receive
    # RecvTread(s).start()
    return s

if __name__ == '__main__':
    s = subscribe()
    testCharge(s)
    # lowPower(s)
# -*- coding: utf-8 -*-
import time
import yaml
from socket import *
from case.testCharge_bak import testCharge
from comn.configRead import Read
from comn.pack2bytes import pack2bytes
from comn.receive2dic import RecvTread
import hashlib

  # ------------------------------------
  # Name:         bukesi
  # Description: 更新配置文件，以yaml形式存储
  # Author:       kingming
  # Date:         2020/4/10
  # ------------------------------------


# 读取配置文件(config.yaml)
with open('conf/config.yaml') as yfile:
    try:
        yobj = yaml.safe_load(yfile)
        server_ip = yobj.get('server_ip')
    except yaml.YAMLError as error:
        print error
# 过滤消息
set_filter = {"message_type": "set_filter", "filter":["sensor_data", "laser", "report_sensor_data_info", "all_file_info", "report_obd_status", "set_sensor_data_info", "report_basic_status", 'sensor_power_status', 'report_stat', 'report_pos_vel_status', 'auto_guided_task_status', 'device_status', 'local_path', 'register_status', 'all_robot_info', 'sonar', 'config_signature']}

def subscribe():
    # Socket TCP
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_ip, 6789))
    # status
    json_packed = pack2bytes(yobj.get('reg_client_message'))  # 注册客户端
    s.send(json_packed)
    json_packed = pack2bytes(set_filter)  # 过滤消息
    s.send(json_packed)
    RecvTread(s).start()
    return s


if __name__ == '__main__':
    s = subscribe()
    json_packed = pack2bytes(yobj.get('get_file')) # 获取点位信息
    s.send(json_packed)
    json_packed = pack2bytes(yobj.get('get_all_robot_info_message'))
    s.send(json_packed)
    # testCharge(s)
    # lowPower(s)
    # testMd5()
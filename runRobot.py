# -*- coding: utf-8 -*-
from socket import *
from case.testCharge import testCharge
from comn.configRead import Read
from comn.pack2bytes import pack2bytes
from comn.receive2dic import RecvTread

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
set_filter = {"message_type": "set_filter","filter": ["laser", "all_file_info", "report_sensor_data_info",   "set_sensor_data_info", "report_basic_status", "report_obd_status", 'sensor_power_status', 'report_stat',   'report_pos_vel_status', 'auto_guided_task_status', 'device_status', 'local_path', 'register_status', 'all_robot_info',   'sonar']}

def subscribe():
    # Socket TCP
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_ip, 6789))
    # status
    json_packed = pack2bytes(R.getInfo('status', 'reg_client_message'))  # 注册客户端
    s.send(json_packed)
    json_packed = pack2bytes(set_filter)  # 过滤消息
    s.send(json_packed)
    # print R.getInfo('control', 'move')
    # json_packed = pack2bytes(R.getInfo('control', 'move'))  # 移动一段距离
    # s.send(json_packed)
    # time.sleep(0.2)
    # json_packed = pack2bytes(R.getInfo('control', 'move'))  # 移动一段距离
    # s.send(json_packed)
    # time.sleep(0.2)
    # json_packed = pack2bytes(R.getInfo('control', 'move'))  # 移动一段距离
    # s.send(json_packed)
    # time.sleep(0.2)
    # json_packed = pack2bytes(R.getInfo('control', 'move'))  # 移动一段距离
    # s.send(json_packed)
    # time.sleep(0.2)
    # json_packed = pack2bytes(R.getInfo('control', 'move'))  # 移动一段距离
    # s.send(json_packed)
    # json_packed = pack2bytes(R.getInfo('status', 'get_all_robot_info_message'))  # 获取全部机器人信息
    # s.send(json_packed)
    # json_packed = pack2bytes(R.getInfo('status', 'report_loc_status'))  # 定位状态
    # s.send(json_packed)
    # json_packed = pack2bytes(R.getInfo('status', 'move_status'))  # 移动状态
    # s.send(json_packed)
    # json_packed = pack2bytes(R.getInfo('status', 'charge_status'))  # 充电状态
    # s.send(json_packed)
    # json_packed = pack2bytes(R.getInfo('status', 'move_status1'))
    # s.send(json_packed)
    # # 启动接收线程
    # RecvTread(s).start()
    return s

if __name__ == '__main__':
    s = subscribe()
    testCharge(s)
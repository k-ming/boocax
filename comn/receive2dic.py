# -*- coding: utf-8 -*-#
import json
import struct
from threading import Thread
from comn.getDate import getDate

2
3  #------------------------------------
4  # Name:         receive2dic
5  # Description:  
6  # Author:       kingming
7  # Date:         2020/5/21
8  #------------------------------------

def receive2dic(tcp_sock):
    """ 以字节方式（bytes）接收数据，
    返回 “字典”（python 的 key-value 数据类型） """
    # 接收 4 字节的固定头部
    head_bytes = tcp_sock.recv(4)
    while 4 - head_bytes.__len__():
        head_bytes += tcp_sock.recv(4 - head_bytes.__len__())
    head_int = struct.unpack('=L', head_bytes)[0]
    # # 接收消息体
    buffer = []
    message_len = 0
    while head_int - message_len:
        data_byte = tcp_sock.recv(head_int - message_len)
        buffer.append(data_byte)
        message_len += data_byte.__len__()
        # 拼接字符串与编码转换
    str_json = (b''.join(buffer)).decode()
    return json.loads(str_json)


class RecvTread(Thread):
    def __init__(self, tcp_socket):
        Thread.__init__(self)
        self.s = tcp_socket

    def run(self):
        while True:
            msg = receive2dic(self.s)
            if msg['message_type'] == 'register_status':
                print getDate(), '客户端注册成功:{}'.format(msg)
            elif msg['message_type'] == 'all_robot_info':
                print getDate(), '获取服务器上所有机器人:{}'.format(msg)
            elif msg['message_type'] == 'report_charge_status':
                print getDate(), '充电状态:{}'.format(msg)
            elif msg['message_type'] == 'report_move_status_v2' or msg['message_type'] == 'report_move_status':
                print getDate(), '移动状态:{}'.format(msg)
            elif msg['message_type'] == 'sonar':
                print getDate(), '超声:{}'.format(msg)
            elif msg['message_type'] == 'report_pos_vel_status':
                print getDate(), '机器人位置与速度状态更新:{}'.format(msg)
            elif msg['message_type'] == 'auto_guided_task_status':
                print getDate(), '状态反馈(上传到Server):{}'.format(msg)
            elif msg['message_type'] == 'report_pos_vel_status':
                print getDate(), '位置速度信息:{}'.format(msg)
            elif msg['message_type'] == 'report_sensor_data_info':
                print getDate(), '超声传感器:{}'.format(msg)
            elif msg['message_type'] == 'report_basic_status':
                print getDate(), '基本信息:{}'.format(msg)
            elif msg['message_type'] == 'device_status':
                print getDate(), '设备状态:{}'.format(msg)
            elif msg['message_type'] == 'laser':
                print getDate(), '激光雷达数据（laser）:{}'.format(msg)
            elif msg['message_type'] == 'report_button_status':
                print getDate(), '急停状态:{}'.format(msg)
            elif msg['message_type'] == 'report_fault_code':
                if msg['code'] == 1:
                    print getDate(), '充电失败:{}'.format(msg)
                else:
                    print getDate(), '硬件错误:{}'.format(msg)
            elif msg['message_type'] == 'real_path':
                print getDate(), '全局规划路径:{}'.format(msg)
            elif msg['message_type'] == 'report_poi_status':
                print getDate(), 'POI状态反馈:{}'.format(msg)
            elif msg['message_type'] == 'report_loc_status':
                print getDate(), '机器人定位状态更新:{}'.format(msg)
            elif msg['message_type'] == 'device_task_request':
                print getDate(), '当前任务类型:{}'.format(msg)
            elif msg['message_type'] == 'sensor_power_status':
                print getDate(), '传感器上电状态:{}'.format(msg)
            elif msg['message_type'] == 'report_obd_status':
                print getDate(), 'obd信息:{}'.format(msg)
            elif msg['message_type'] == 'local_path':
                print getDate(), '（导航中）局部路径:{}'.format(msg)
            else:
                print getDate(), msg
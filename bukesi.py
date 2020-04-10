# -*- coding: utf-8 -*-
2
3  #------------------------------------
4  # Name:         bukesi
5  # Description:  
6  # Author:       kingming
7  # Date:         2020/4/10
8  #------------------------------------

import time
import json
import struct
from socket import *
from threading import Thread

server_ip = '192.168.50.138' # 修改为服务器 ip
# Mac
host_mac = '00:8B:92:3E:56:33' # 修改为本机 mac
robot_mac = '02:38:4B:4A:55:0C' # 修改为实际机器人的 mac

# 命令
reg_client_message = {
 "message_type": "register_client",
 "client_type": 3,
 "mac_address": host_mac}
get_all_robot_info_message = {
 "message_type": "get_all_robot_info",}
move_message = {
 "message_type": "move",
 "robot_mac_address": robot_mac,
 "vx": 0,
 "vy": 0,
 'vtheta': 0.2}

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

def pack2bytes(dic_ready):
    """ 将 JSON 消息打包成（含固定头部的）字节（bytes）数据 """
    json_str = json.dumps(dic_ready)  # Python 数据格式（dict） -> JSON 字符串
    json_bytes = json_str.encode()  # 字符串 转换编码为 bytes 格式
    # Head
    json_bytes_len = len(json_bytes)  # 计算消息的字节（bytes）长度
    message_packed = struct.pack('=L', json_bytes_len) + json_bytes
    return message_packed
    # return json_bytes

class RecvTread(Thread):
    def __init__(self, tcp_socket):
        Thread.__init__(self)
        self.s = tcp_socket

    def run(self):
        while True:
            msg = receive2dic(self.s)
            time.sleep(1)
            # print(msg['message_type'])
            print msg

if __name__ == '__main__':
    # Socket TCP
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_ip, 6789))

    # Send
    json_packed = pack2bytes(reg_client_message)  # 注册客户端
    s.send(json_packed)
    # json_packed = pack2bytes(get_all_robot_info_message)  # 获取全部机器人信息
    # s.send(json_packed)

    # 启动接收线程
    RecvTread(s).start()

    # 移动控制
    # json_packed = pack2bytes(move_message)
    # while True:
    #     s.send(json_packed)
    #     time.sleep(0.2)
        # time.sleep(1000)

    # Close
    # s.close()
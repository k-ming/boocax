# -*- coding: utf-8 -*-
from socket import *
from configRead import Read
import time
import json
import struct
from threading import Thread

3  # ------------------------------------
4  # Name:         bukesi
5  # Description:  
6  # Author:       kingming
7  # Date:         2020/4/10
8  # ------------------------------------


# 读取配置文件
R = Read('config.ini')
server_ip = R.getInfo('info', 'server_ip')

# 过滤消息
set_filter = {"message_type": "set_filter","filter": ["laser", "all_file_info", "report_sensor_data_info",   "set_sensor_data_info", "report_basic_status", "report_obd_status", 'sensor_power_status', 'report_stat',   'report_pos_vel_status', 'auto_guided_task_status', 'device_status', 'local_path', 'register_status', 'all_robot_info',   'sonar']}
def getDate():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def writeLog(content):
    f1 = open('logs/boocax_'+time.strftime('%Y-%m-%d', time.localtime())+'.log', 'a+')
    f1.write(getDate()+':'+str(content)+'\n')
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
            else:
                print getDate(), msg
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
    RecvTread(s).start()
    return s

def statTest():
    s = subscribe()
    i = 1
    fail = 0
    while i <= 50:
        print '*****************开始第%d轮导航****************************'%i
        writeLog('*****************开始第%d轮导航****************************'%i)
        print '>>>导航到p17...'
        writeLog('>>>导航到p17...')
        json_packed = pack2bytes(R.getInfo('control', 'poi_action2'))  # 导航点指定点
        s.send(json_packed)
        while True:
            msg = receive2dic(s)
            writeLog(msg)
            if msg['message_type'] == 'report_move_status_v2':
                if msg['move_status'] == 300:
                    print '到达目的地,状态:{}'.format(msg['move_status'])
                    writeLog('到达目的地p2')
                    break
            else:
                print '导航中...'
                writeLog('导航中...')
                continue
        time.sleep(6)

        print '>>>导航到充电点并充电...'
        writeLog('>>>导航到充电点并充电(charge)...')
        json_packed = pack2bytes(R.getInfo('control', 'goCharge'))  # 导航到对桩点并充电
        s.send(json_packed)
        while True:
            msg = receive2dic(s)
            writeLog(msg)
            if msg['message_type'] == 'report_charge_status':
                if msg['charge_status'] == 1:
                    print '正在使用充电桩充电(自动对接),充电状态:{}'.format(msg['charge_status'])
                    writeLog('正在使用充电桩充电(自动对接),充电状态:{}'.format(msg['charge_status']))
                    break
                elif msg['charge_status'] == 6:
                    print '充电状态：正在使用充电桩充电（手动对接),充电状态:{}'.format(msg['charge_status'])
                    writeLog('充电状态：正在使用充电桩充电（手动对接),充电状态:{}'.format(msg['charge_status']))
                    break
                elif msg['charge_status'] == 3:
                    print '对接过程中：正在和充电座对接,充电状态:{}'.format(msg['charge_status'])
                    writeLog('对接过程中：正在和充电座对接,充电状态:{}'.format(msg['charge_status']))
                    continue
                elif msg['charge_status'] == 8:
                    print '自动充电测试红外信号状态:{}'.format(msg['charge_status'])
                    writeLog('自动充电测试红外信号状态:{}'.format(msg['charge_status']))
                    continue
                elif msg['charge_status'] == 0:
                    print '充电失败，未充电状态:{}'.format(msg['charge_status'])
                    writeLog('充电失败，未充电状态:{}'.format(msg['charge_status']))
                    fail += 1
                    break
            elif msg['message_type'] == 'report_fault_code':
                if msg['code'] == 1:
                    print getDate(), '充电失败:{}'.format(msg)
                    fail += 1
                    break
                elif msg['code'] == 141:
                    print '未检测到充电桩信号（红外信号测试错误）'
                    fail += 1
                    break
                elif msg['code'] == 142:
                    print '前往充电桩耗时超时'
                    fail += 1
                    break
                elif msg['code'] == 143:
                    print '对接失败'
                    fail += 1
                    break
                elif msg['code'] == 144:
                    print '自动充电对接成功后 但在充电中与充电桩脱落'
                    fail += 1
                    break
                else:
                    print getDate(), '硬件错误:{}'.format(msg)
                    continue
            elif msg['message_type'] == 'report_move_status_v2':
                if msg['move_status'] == 300:
                    print '到达对位点'
                    writeLog('到达对位点')
                    continue
            else:
                print '导航到对位点...'
                writeLog('导航到对位点...')
                continue
        time.sleep(10)
        print '取消充电...'
        json_packed = pack2bytes(R.getInfo('control', 'cancel_charge'))  # 取消充电
        s.send(json_packed)
        time.sleep(10)
        # json_packed = pack2bytes(R.getInfo('control', 'poi_action1'))  # 导航到点
        # s.send(json_packed)
        i += 1
    print '*********************已完成{}轮导航,充电失败{}次*****************************'.format(i-1, fail)
    writeLog('*********************已完成{}轮导航,充电失败{}次*****************************'.format(i-1, fail))
    # Close
    s.close()

if __name__ == '__main__':
    s = subscribe()
    # statTest()
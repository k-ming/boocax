# -*- coding: utf-8 -*-#
import json
import yaml
import struct
import time, sys
from comn.configRead import Read
from threading import Thread
from comn.getDate import getDate
from comn.setYaml import setDictYaml
from comn.writeLog import writeLog

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
2
3  #------------------------------------
4  # Name:         receive2dic
5  # Description:  
6  # Author:       kingming
7  # Date:         2020/5/21
8  #------------------------------------
R = Read("") # 需要使用其中的方法解析base64
f1 = open('conf/config.yaml')
ymload = yaml.safe_load(f1)
poi_info = ymload.get('poi_info')
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
    
def udecode(utext):
    # 去掉dict中Unicode编码符号
    return json.dumps(utext).encode('utf-8').decode('unicode-escape')

# 将坐标转化为名称
def poiNmae(poi):
    global poi_info
    # print poi_info
    x, y, yaw = poi.get('x'), poi.get('y'), poi.get('yaw')
    # print x, y, yaw
    for v in poi_info:
        if v.get('position').get('x') == x and v.get('position').get('y') == y and v.get('position').get('yaw') == yaw:
            return v.get('name')
            break
        else:
            continue
    return udecode(poi)

class RecvTread(Thread):
    def __init__(self, tcp_socket):
        Thread.__init__(self)
        self.s = tcp_socket

    def run(self):
        while True:
            msg = receive2dic(self.s)
            if msg['message_type'] == 'register_status':
                print(getDate(), '客户端注册成功:{}'.format((udecode(msg))))
            elif msg['message_type'] == 'all_robot_info':
                print(getDate(), '获取服务器上所有机器人:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'report_charge_status':
                print(getDate(), '充电状态:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'report_move_status_v2' or msg['message_type'] == 'report_move_status':
                print(getDate(), '移动状态:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'sonar':
                print(getDate(), '超声:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'report_pos_vel_status':
                print(getDate(), '机器人位置与速度状态更新:{}'.format(udecode(msg['pose'])))
                print('转化后的坐标：{},{}'.format(1338/2 + msg['pose']['x']*20, 898-(msg['pose']['y']*20 + 898/2)))
                # print '转化后的坐标：{},{}'.format(-1338/2 + msg['pose']['x']*20, 898/2-msg['pose']['y']*20)
            elif msg['message_type'] == 'auto_guided_task_status':
                print(getDate(), '状态反馈(上传到Server):{}'.format(udecode(msg)))
            elif msg['message_type'] == 'report_pos_vel_status':
                print(getDate(), '位置速度信息:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'report_sensor_data_info':
                print(getDate(), '超声传感器:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'report_basic_status':
                print(getDate(), '基本信息:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'device_status':
                print(getDate(), '设备状态:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'laser':
                print(getDate(), '激光雷达数据（laser）:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'report_button_status':
                print(getDate(), '急停状态:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'report_fault_code':
                if msg['code'] == 1:
                    print(getDate(), '充电失败:{}'.format(udecode(msg)))
                else:
                    print(getDate(), '硬件错误:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'real_path':
                print(getDate(), '全局规划路径 ——————————————————>:{}'.format( poiNmae(msg['real_path_info'][-1]) ))
            elif msg['message_type'] == 'report_poi_status':
                print(getDate(), 'POI状态反馈:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'report_loc_status':
                print(getDate(), '机器人定位状态更新:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'device_task_request':
                print(getDate(), '当前任务类型:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'sensor_power_status':
                print(getDate(), '传感器上电状态:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'report_obd_status':
                print(getDate(), 'obd信息:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'local_path':
                print(getDate(), '（导航中）局部路径:{}'.format(udecode(msg)))
            elif msg['message_type'] == 'update_file':
                if msg['file_name'] == 'poi.json':
                    print(getDate(), '更新点位信息:{}'.format( json.loads(R.getBase64(udecode( msg['content'])))['poi_info']  )) 
                    setDictYaml('conf/config.yaml', 'poi_info', json.loads(R.getBase64(udecode( msg['content'])))['poi_info'])
                    # print(getDate(), '更新充电点坐标:{}'.format( json.loads(R.getBase64(udecode( msg['content'])))['charge_points_info'][0]['name'] ))
                    # setDictYaml('conf/config.yaml', 'charge_point', json.loads(R.getBase64(udecode( msg['content'])))['charge_points_info'][0]['name'] ) 
                elif msg['file_name'] == 'map.png':
                    print(getDate(), '地图图片:{}'.format(udecode(msg['content'])) )
                else :
                    print(getDate(), '文件信息:{}'.format(udecode(msg)) )
            elif msg['message_type'] == 'all_map_info':
                print(getDate(), '所有地图信息:{}'.format(udecode(msg)) )
            else:
                print(getDate(), udecode(msg) )


# if __name__ == '__main__':
#     p = {"y": -5.15, "x": 16.85, "yaw": 3.14}
#     print poiNmae(p)
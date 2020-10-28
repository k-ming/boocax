# -*- coding: utf-8 -*-
import time
import yaml
from socket import *
from case.testCharge_bak import testCharge
from case.testPower import testPower
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
set_filter = {"message_type": "set_filter", "filter":["sensor_data", "laser", "all_file_info",  "set_sensor_data_info", "report_basic_status", 'sensor_power_status', 'report_stat', 'device_status', 'local_path', 'register_status', 'all_robot_info', 'sonar','config_signature',"report_obd_status","report_loc_status", 'report_pos_vel_status','auto_guided_task_status','report_sensor_data_info']}

# , ""
# ["如何领取营业执照","企业设立、变更（备案）、注销、企业登记咨询","CA证书（法人一证通）","食品经营许可证","档案查询","装修备案","领取税务Ukey","税务Ukey初始密码"]
# ["文化事业建设费的免征期限","已征的文化事业建设费如何处理","哪些纳税人可以选择综合申报","纳税人选择税种综合申报需要办理的手续","新办企业提交哪些材料","注明了旅客身份信息的火车票补票是否可作为国内旅客运输服务进项抵扣凭证","2019年以前的个人所得税纳税证明（纳税清单）在哪里开具","需同时申报缴纳企业所得税（预缴）、城镇土地使用税、房产税、土地增值税、印花税中多个税种的纳税人，必须进行综合申报吗","城乡居民需要去哪里办理参保信息登记"]

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
    json_packed = pack2bytes(yobj.get('get_poi')) # 更新本地点位信息
    s.send(json_packed)
    # json_packed = pack2bytes(yobj.get('update_file')) # 更新pol.json
    # s.send(json_packed)
    # json_packed = pack2bytes(yobj.get('continue_roaming')) # 继续漫游
    # s.send(json_packed)
    # json_packed = pack2bytes(yobj.get('get_map') ) # 获取地图图片
    # s.send(json_packed)
    json_packed = pack2bytes(yobj.get('get_all_robot_info'))
    s.send(json_packed)
    # testCharge(s)
    # lowPower(s)
    # testPower(s, 10)
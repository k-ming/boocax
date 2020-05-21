# -*- coding: utf-8 -*-#
import json
import struct

3  #------------------------------------
4  # Name:         pack2bytes
5  # Description:  
6  # Author:       kingming
7  # Date:         2020/5/21
8  #------------------------------------

def pack2bytes(dic_ready):
    """ 将 JSON 消息打包成（含固定头部的）字节（bytes）数据 """
    json_str = json.dumps(dic_ready)  # Python 数据格式（dict） -> JSON 字符串
    json_bytes = json_str.encode()  # 字符串 转换编码为 bytes 格式
    # Head
    json_bytes_len = len(json_bytes)  # 计算消息的字节（bytes）长度
    message_packed = struct.pack('=L', json_bytes_len) + json_bytes
    return message_packed
    # return json_bytes
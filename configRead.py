# -*- coding: utf-8 -*-#
2
3  #------------------------------------
4  # Name:         configRead
5  # Description:  
6  # Author:       kingming
7  # Date:         2020/4/14
8  #------------------------------------

import configparser
import re


class Read():
    def __init__(self, file):
        self.cfg = configparser.ConfigParser()
        self.cfg.read('config.ini', encoding="utf-8")

    def getInfo(self, c1, c2):
        if c1 == 'info':
            return self.cfg.get(c1, c2).encode('utf-8')
        elif c1 == 'status':
            return eval(self.cfg.get(c1, c2).encode('utf-8').replace('host_mac', self.getInfo('info', 'host_mac')))
        elif c1 == 'control':  # 正则匹配
            rec = re.search('"robot_mac_address":(.*?),', self.cfg.get(c1, c2).encode('utf-8')).group(1)
            return eval(re.sub(rec, self.getInfo('info', 'robot_mac1'), self.cfg.get(c1, c2).encode('utf-8')))
        else:
            print '没有匹配到结果...'


# if __name__ == '__main__':
#     R = Read('config.ini')
#     print R.getInfo('control', 'poi_action1')


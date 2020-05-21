# -*- coding: utf-8 -*-#
from threading import Thread
from comn.configRead import Read
3  #------------------------------------
4  # Name:         testThred
5  # Description:  
6  # Author:       kingming
7  # Date:         2020/5/21
8  #------------------------------------

class ReadConfig(Thread):
    def __init__(self, info, param):
        Thread.__init__(self)
        self.s = info
        self.p = param

    def run(self):
        while True:
            r = Read('../conf/config.ini')
            print r.getInfo(self.s, self.p)


if __name__ == '__main__':
    R1 = ReadConfig('info', 'robot_mac1')
    R1.start()
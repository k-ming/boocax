# -*- coding: utf-8 -*-#
import time

3  #------------------------------------
4  # Name:         getDate
5  # Description:  
6  # Author:       kingming
7  # Date:         2020/5/21
8  #------------------------------------

def getDate():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
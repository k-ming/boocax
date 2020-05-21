# -*- coding: utf-8 -*-#
import time
from comn.getDate import getDate

3  #------------------------------------
4  # Name:         writeLog
5  # Description:  
6  # Author:       kingming
7  # Date:         2020/5/21
8  #------------------------------------

def writeLog(content):
    f1 = open('logs/boocax_'+time.strftime('%Y-%m-%d', time.localtime())+'.log', 'a+')
    f1.write(getDate()+':'+str(content)+'\n')
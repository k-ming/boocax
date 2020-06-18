# -*- coding: utf-8 -*-#
import time
from comn.writeLog import writeLog
from comn.pack2bytes import pack2bytes
from comn.receive2dic import receive2dic
from comn.getDate import getDate
from comn.configRead import Read

2
3  # ------------------------------------
4  # Name:         test_auto_charge
5  # Description:  
6  # Author:       kingming
7  # Date:         2020/5/21
8  # ------------------------------------


def testCharge(s):
    R = Read('conf/config.ini')
    s = s
    i = 1
    fail = 0
    while i <= 20:
        print getDate(),'*****************开始第%d轮导航****************************' % i
        writeLog('*****************开始第%d轮导航****************************' % i)
        print getDate(), '>>>导航到p2...'
        writeLog('>>>导航到p2...')
        json_packed = pack2bytes(R.getInfo('control', 'poi_action2'))  # 导航点指定点
        s.send(json_packed)
        while True:
            msg = receive2dic(s)
            writeLog(msg)
            if msg['message_type'] == 'report_move_status_v2':
                if msg['move_status'] == 300:
                    print getDate(), '到达目的地,状态:{}'.format(msg['move_status'])
                    writeLog('到达目的地p2:{}'.format(msg['move_status']))
                    break
            elif msg['message_type'] == 'report_button_status':
                if msg['emergency_button'] == 2:
                    print getDate(), '急停被按下, 导航取消...:{}'.format(msg['emergency_button'])
                    writeLog('error: 急停被按下, 导航取消...:{}'.format(msg['emergency_button']))
                else:
                    print getDate(), '急停拔起, 继续导航...:{}'.format(msg['emergency_button'])
                    writeLog('急停拔起, 继续导航...:{}'.format(msg['emergency_button']))
            else:
                print getDate(), '导航中...'
                writeLog('导航中...')
                continue
        time.sleep(6)

        print getDate(), '>>>导航到充电点并充电...'
        writeLog('>>>导航到充电点并充电(charge)...')
        json_packed = pack2bytes(R.getInfo('control', 'goCharge'))  # 导航到对桩点并充电
        s.send(json_packed)
        while True:
            msg = receive2dic(s)
            writeLog(msg)
            if msg['message_type'] == 'report_charge_status':
                if msg['charge_status'] == 1:
                    print getDate(),'正在使用充电桩充电(自动对接),充电状态:{}'.format(msg['charge_status'])
                    writeLog('正在使用充电桩充电(自动对接),充电状态:{}'.format(msg['charge_status']))
                    break
                elif msg['charge_status'] == 6:
                    print getDate(), '充电状态：正在使用充电桩充电（手动对接),充电状态:{}'.format(msg['charge_status'])
                    writeLog('充电状态：正在使用充电桩充电（手动对接),充电状态:{}'.format(msg['charge_status']))
                    break
                elif msg['charge_status'] == 3:
                    print getDate(), '对接过程中：正在和充电座对接,充电状态:{}'.format(msg['charge_status'])
                    writeLog('对接过程中：正在和充电座对接,充电状态:{}'.format(msg['charge_status']))
                    continue
                elif msg['charge_status'] == 8:
                    print getDate(), '自动充电测试红外信号状态:{}'.format(msg['charge_status'])
                    writeLog('自动充电测试红外信号状态:{}'.format(msg['charge_status']))
                    continue
                elif msg['charge_status'] == 0:
                    print getDate(), '充电失败，未充电状态:{}'.format(msg['charge_status'])
                    writeLog('error: 充电失败，未充电状态:{}'.format(msg['charge_status']))
                    fail += 1
                    break
            elif msg['message_type'] == 'report_fault_code':
                if msg['code'] == 1:
                    print getDate(), '充电失败:{}'.format(msg['code'])
                    writeLog('error: 充电失败:{}'.format(msg['code']))
                    fail += 1
                    break
                elif msg['code'] == 141:
                    print getDate(), '未检测到充电桩信号（红外信号测试错误):{}'.format(msg['code'])
                    writeLog('error: 未检测到充电桩信号（红外信号测试错误):{}'.format(msg['code']))
                    fail += 1
                    break
                elif msg['code'] == 142:
                    print '前往充电桩耗时超时:{}'.format(msg['code'])
                    writeLog('error: 前往充电桩耗时超时:{}'.format(msg['code']))
                    fail += 1
                    break
                elif msg['code'] == 143:
                    print getDate(), '对接失败:{}'.format(msg['code'])
                    writeLog('error: 对接失败:{}'.format(msg['code']))
                    fail += 1
                    break
                elif msg['code'] == 144:
                    print getDate(), '自动充电对接成功后 但在充电中与充电桩脱落:{}'.format(msg['code'])
                    writeLog('error:自动充电对接成功后 但在充电中与充电桩脱落:{}'.format(msg['code']))
                    fail += 1
                    break
                else:
                    print getDate(), '硬件错误:{}'.format(msg)
                    writeLog('warn: 硬件错误:{}'.format(msg))
                    continue
            elif msg['message_type'] == 'report_move_status_v2':
                if msg['move_status'] == 300:
                    print getDate(), '到达对位点:{}'.format(msg['move_status'])
                    writeLog('到达对位点:{}'.format(msg['move_status']))
                    continue
            else:
                print getDate(), '导航到对位点...'
                writeLog('导航到对位点...')
                continue
        time.sleep(10)
        print getDate(), '取消充电...'
        json_packed = pack2bytes(R.getInfo('control', 'cancel_charge'))  # 取消充电
        s.send(json_packed)
        time.sleep(10)
        # json_packed = pack2bytes(R.getInfo('control', 'poi_action1'))  # 导航到点
        # s.send(json_packed)
        i += 1
    print getDate(), '*********************已完成{}轮导航,充电失败{}次*****************************'.format(i - 1, fail)
    writeLog('*********************已完成{}轮导航,充电失败{}次*****************************'.format(i - 1, fail))
    # Close
    s.close()

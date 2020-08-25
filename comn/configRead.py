# -*- coding: utf-8 -*-#
import base64

import configparser
import re
import hashlib
3  #------------------------------------
4  # Name:         configRead
5  # Description:  
6  # Author:       kingming
7  # Date:         2020/4/14
8  #------------------------------------

class Read():
    def __init__(self, file):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(file, encoding="utf-8")

    def getInfo(self, c1, c2):
        if c1 == 'info':
            return self.cfg.get(c1, c2).encode('utf-8')
        elif c1 == 'status':
            return eval(self.cfg.get(c1, c2).encode('utf-8').replace('host_mac', self.getInfo('info', 'host_mac')))
        elif c1 == 'control':  # 正则匹配
            rec = re.search('"robot_mac_address":(.*?),', self.cfg.get(c1, c2).encode('utf-8')).group(1)
            return eval(re.sub(rec, self.getInfo('info', 'robot_mac'), self.cfg.get(c1, c2).encode('utf-8')))
        else:
            print '没有匹配到结果...'
    def setInfo(self, c1, c2):
        if c1 not in self.cfg.sections():
            print 'not found options'
        else:
            print self.getInfo(c1, c2)
            self.cfg.set('status', 'update_file','test')

    # update_file = {"message_type": "update_file", "file_name": "poi.json", "md5": "e99a18c428cb38d5f260853678922e03",
    #                "content": u"eyJ2ZXJzaW9uIjogIjEuMC4wIiwgImVuY29kaW5nIjogInV0Zi04IiwgInBvaV9pbmZvIjogW3sibmFtZSI6ICJwMSIsICJwb3NpdGlvbiI6IHsieCI6IC0yMS41NCwgInkiOiA5LjQ3LCAieWF3IjogMC4wMn19LCB7Im5hbWUiOiAicDIiLCAicG9zaXRpb24iOiB7IngiOiAtMjEuMzMsICJ5IjogNy43MywgInlhdyI6IDUuOTN9fSwgeyJuYW1lIjogInAzIiwgInBvc2l0aW9uIjogeyJ4IjogLTIxLjM4LCAieSI6IDYuNDgsICJ5YXciOiA2LjE2fX0sIHsibmFtZSI6ICJwNCIsICJwb3NpdGlvbiI6IHsieCI6IC0xNi4yMiwgInkiOiA1LjIsICJ5YXciOiAwLjA2fX0sIHsibmFtZSI6ICJwNSIsICJwb3NpdGlvbiI6IHsieCI6IC0xMi42MywgInkiOiA1LjE1LCAieWF3IjogNi4yN319LCB7Im5hbWUiOiAicDYiLCAicG9zaXRpb24iOiB7IngiOiAtOS4zMywgInkiOiA1LjIsICJ5YXciOiAwLjA1fX0sIHsibmFtZSI6ICJ3b3JrIiwgInBvc2l0aW9uIjogeyJ4IjogLTAuNTgsICJ5IjogNS4xNywgInlhdyI6IDAuMDl9fSwgeyJuYW1lIjogInA3IiwgInBvc2l0aW9uIjogeyJ4IjogLTYuMjksICJ5IjogNS4wNywgInlhdyI6IDYuMjd9fSwgeyJuYW1lIjogInA4IiwgInBvc2l0aW9uIjogeyJ4IjogLTMuMTgsICJ5IjogNS4wLCAieWF3IjogMC4yMn19LCB7Im5hbWUiOiAiY2FyNiIsICJwb3NpdGlvbiI6IHsieCI6IC0yMS4zMiwgInkiOiA4Ljg1LCAieWF3IjogNi4yMX19LCB7Im5hbWUiOiAiY2FyNCIsICJwb3NpdGlvbiI6IHsieCI6IC0xOC4yMywgInkiOiA1LjIzLCAieWF3IjogMy4xMX19LCB7Im5hbWUiOiAiaG9tZSIsICJwb3NpdGlvbiI6IHsieCI6IC05LjYxLCAieSI6IDEwLjQ2LCAieWF3IjogMC4wNX19LCB7Im5hbWUiOiAiY2FyNSIsICJwb3NpdGlvbiI6IHsieCI6IC0yMS4zOSwgInkiOiA3LjAyLCAieWF3IjogNi4xOX19LCB7Im5hbWUiOiAiY2FyMiIsICJwb3NpdGlvbiI6IHsieCI6IC0xMS40LCAieSI6IDUuMjksICJ5YXciOiAzLjI0fX0sIHsibmFtZSI6ICJjYXIzIiwgInBvc2l0aW9uIjogeyJ4IjogLTE0LjQ1LCAieSI6IDUuMTUsICJ5YXciOiAzLjAzfX0sIHsibmFtZSI6ICJjYXIxIiwgInBvc2l0aW9uIjogeyJ4IjogLTguMDYsICJ5IjogNS4yNSwgInlhdyI6IDMuMn19XSwgImNoYXJnZV9wb2ludHNfaW5mbyI6IFt7Im5hbWUiOiAiY2hhcmdlIiwgInBvc2l0aW9uIjogeyJ4IjogLTE5LjIyMTEsICJ5IjogNC45NzE1NSwgInlhdyI6IDEuNDgxNzZ9fV0sICJncm91cHMiOiB7IiNraW5nbWluZyMiOiBbInAxIiwgInAyIiwgInAzIiwgInA0IiwgInA1IiwgInA2IiwgInA3IiwgInA4IiwgIndvcmsiLCAiaG9tZSIsICJjYXIxIiwgImNhcjIiLCAiY2FyMyIsICJjYXI0IiwgImNhcjUiLCAiY2FyNiJdfX0=",
    #                "destination": "both", "file_size": 1536, "version": 1}

    # 设置md5
    def setMd5(self, content):
        m2 = hashlib.md5()
        if not isinstance(content, bytes):
            content = str(content).encode('utf-8')
        m2.update(content)
        return m2.hexdigest()

    def setBase64(self, text):
        return base64.b64encode(str(text))

    def getBase64(self, text):
        return base64.b64decode(text)

if __name__ == '__main__':
    R = Read('../conf/config.ini')
    # str1 = '{"version": "1.0.0", "encoding": "utf-8", "poi_info": [{"name": "p1", "position": {"x": -15.7793, "y": -2.59556, "yaw": 5.98425}}, {"name": "p2", "position": {"x": -16.0159, "y": -0.0725687, "yaw": 6.26617}}, {"name": "p3", "position": {"x": -16.0567, "y": 2.34645, "yaw": 0.0885736}}, {"name": "p4", "position": {"x": -15.9679, "y": 4.93371, "yaw": 0.0856446}}, {"name": "p5", "position": {"x": -13.6906, "y": 5.20321, "yaw": 0.196263}}, {"name": "p6", "position": {"x": -11.6654, "y": 5.15249, "yaw": 0.00583948}}, {"name": "work", "position": {"x": -0.58, "y": 5.17, "yaw": 0.09}}, {"name": "p7", "position": {"x": -9.84174, "y": 5.15823, "yaw": 6.24361}}, {"name": "p8", "position": {"x": -7.82646, "y": 5.11801, "yaw": 6.23384}}, {"name": "car6", "position": {"x": -5.99713, "y": 5.11414, "yaw": 6.21452}}, {"name": "car4", "position": {"x": -2.50368, "y": 5.22152, "yaw": 6.23117}}, {"name": "home", "position": {"x": -9.61, "y": 10.46, "yaw": 0.05}}, {"name": "car5", "position": {"x": -3.96222, "y": 5.261, "yaw": 6.28284}}, {"name": "car2", "position": {"x": -11.4, "y": 5.29, "yaw": 3.24}}, {"name": "car3", "position": {"x": -14.45, "y": 5.15, "yaw": 3.03}}, {"name": "car1", "position": {"x": -8.06, "y": 5.25, "yaw": 3.2}}], "charge_points_info": [{"name": "charge", "position": {"x": -12.7257, "y": 9.1063, "yaw": 0.0375451}}], "groups": {"#13_30_20_11#": ["p7", "home", "p6"]}}'
    # print R.setMd5(str1)
    # print R.setBase64(str1)
    # print len(str(str1).encode('utf-8'))
    # b1 = "eyJjaGFyZ2VfcG9pbnRzX2luZm8iOlt7Im5hbWUiOiJjaGFyZ2UiLCJwb3NpdGlvbiI6eyJ4IjotMTIuNzI1NywieSI6OS4xMDYzLCJ5YXciOjAuMDM3NTQ1MX19XSwiZW5jb2RpbmciOiJ1dGYtOCIsImdyb3VwcyI6eyIjMThfMzBfMjBfMDAjIjpbInA1IiwiY2FyMiJdLCIjMTNfNTZfMTRfMTQjIjpbImNhcjUiLCJjYXI0Il0sIiMxNV8zMV8xOF8zMCMiOlsicDUiLCJwNyIsImNhcjYiXSwiIzA5XzMwXzExXzMwIyI6WyJjYXI0IiwiY2FyNSIsImNhcjYiXX0sInBvaV9pbmZvIjpbeyJuYW1lIjoicDEiLCJwb3NpdGlvbiI6eyJ4IjotMTUuNzc5MywieSI6LTIuNTk1NTYsInlhdyI6NS45ODQyNX19LHsibmFtZSI6InAyIiwicG9zaXRpb24iOnsieCI6LTE2LjAxNTksInkiOi0wLjA3MjU2ODcsInlhdyI6Ni4yNjYxN319LHsibmFtZSI6InAzIiwicG9zaXRpb24iOnsieCI6LTE2LjA1NjcsInkiOjIuMzQ2NDUsInlhdyI6MC4wODg1NzM2fX0seyJuYW1lIjoicDQiLCJwb3NpdGlvbiI6eyJ4IjotMTUuOTY3OSwieSI6NC45MzM3MSwieWF3IjowLjA4NTY0NDZ9fSx7Im5hbWUiOiJwNSIsInBvc2l0aW9uIjp7IngiOi0xMy42OTA2LCJ5Ijo1LjIwMzIxLCJ5YXciOjAuMTk2MjYzfX0seyJuYW1lIjoicDYiLCJwb3NpdGlvbiI6eyJ4IjotMTEuNjY1NCwieSI6NS4xNTI0OSwieWF3IjowLjAwNTgzOTQ4fX0seyJuYW1lIjoid29yayIsInBvc2l0aW9uIjp7IngiOi0wLjU4LCJ5Ijo1LjE3LCJ5YXciOjAuMDl9fSx7Im5hbWUiOiJwNyIsInBvc2l0aW9uIjp7IngiOi05Ljg0MTc0LCJ5Ijo1LjE1ODIzLCJ5YXciOjYuMjQzNjF9fSx7Im5hbWUiOiJwOCIsInBvc2l0aW9uIjp7IngiOi03LjgyNjQ2LCJ5Ijo1LjExODAxLCJ5YXciOjYuMjMzODR9fSx7Im5hbWUiOiJjYXI2IiwicG9zaXRpb24iOnsieCI6LTUuOTk3MTMsInkiOjUuMTE0MTQsInlhdyI6Ni4yMTQ1Mn19LHsibmFtZSI6ImNhcjQiLCJwb3NpdGlvbiI6eyJ4IjotMi41MDM2OCwieSI6NS4yMjE1MiwieWF3Ijo2LjIzMTE3fX0seyJuYW1lIjoiaG9tZSIsInBvc2l0aW9uIjp7IngiOi05LjYxLCJ5IjoxMC40NiwieWF3IjowLjA1fX0seyJuYW1lIjoiY2FyNSIsInBvc2l0aW9uIjp7IngiOi0zLjk2MjIyLCJ5Ijo1LjI2MSwieWF3Ijo2LjI4Mjg0fX0seyJuYW1lIjoiY2FyMiIsInBvc2l0aW9uIjp7IngiOi0xMS40LCJ5Ijo1LjI5LCJ5YXciOjMuMjR9fSx7Im5hbWUiOiJjYXIzIiwicG9zaXRpb24iOnsieCI6LTE0LjQ1LCJ5Ijo1LjE1LCJ5YXciOjMuMDN9fSx7Im5hbWUiOiJjYXIxIiwicG9zaXRpb24iOnsieCI6LTguMDYsInkiOjUuMjUsInlhdyI6My4yfX1dLCJ2ZXJzaW9uIjoiMS4wLjAifQ=="
    # print R.getBase64(b1)

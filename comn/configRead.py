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


    # 设置md5
    def setMd5(self, content):
        m2 = hashlib.md5()
        if not isinstance(content, bytes):
            content = str(content).encode('utf-8')
        m2.update(content)
        return m2.hexdigest()

    # 设置base64
    def setBase64(self, text):
        return base64.b64encode(str(text))

    # 解析base64
    def getBase64(self, text):
        return base64.b64decode(text)

if __name__ == '__main__':
    R = Read('../conf/config.ini')
    str1 = '{"version": "1.0.0", "encoding": "utf-8", "poi_info": [{"name": "p1", "position": {"x": 18.95, "y": -5.35, "yaw": 3.14}, "tags": []}, {"name": "p2", "position": {"x": 16.85, "y": -5.35, "yaw": 3.14}, "tags": []}, {"name": "p3", "position": {"x": 14.95, "y": -5.15, "yaw": 3.14}, "tags": []}, {"name": "p4", "position": {"x": 12.95, "y": -5.15, "yaw": 3.14}, "tags": []}, {"name": "p5", "position": {"x": 10.95, "y": -5.15, "yaw": 3.14}, "tags": []}, {"name": "p6", "position": {"x": 8.95, "y": -5.15, "yaw": 3.14}, "tags": []}, {"name": "p7", "position": {"x": 6.95, "y": -5.15, "yaw": 3.14}, "tags": []}, {"name": "p8", "position": {"x": 4.95, "y": -5.15, "yaw": 3.14}, "tags": []}, {"name": "p9", "position": {"x": 2.95, "y": -5.15, "yaw": 0.0}, "tags": []}, {"name": "p10", "position": {"x": -0.15, "y": -4.85, "yaw": 3.14}, "tags": []}, {"name": "p11", "position": {"x": -1.5, "y": -3.05, "yaw": 0.0}, "tags": []}, {"name": "p12", "position": {"x": 0.9, "y": -2.95, "yaw": 3.14}, "tags": []}, {"name": "p13", "position": {"x": 0.7, "y": -0.05, "yaw": 3.14}, "tags": []}, {"name": "p14", "position": {"x": -1.75, "y": -0.05, "yaw": 0.0}, "tags": []}], "charge_points_info": [{"name": "charge", "position": {"x": -12.7446, "y": 9.21743, "yaw": 0.0175081}}], "groups": {"#13_07_15_00#": [], "#15_31_17_00#": [], "#08_54_12_03#": [], "#17_10_20_00#": [], "#red#": ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13", "p14"]}}'
    print R.setMd5(str1)
    print R.setBase64(str1)
    print len(str(str1).encode('utf-8'))
    b1 = "eyJ2ZXJzaW9uIjogIjEuMC4wIiwgImVuY29kaW5nIjogInV0Zi04IiwgInBvaV9pbmZvIjogW3sibmFtZSI6ICJwMSIsICJwb3NpdGlvbiI6IHsieCI6IDE4Ljk1LCAieSI6IC01LjM1LCAieWF3IjogMy4xNH0sICJ0YWdzIjogW119LCB7Im5hbWUiOiAicDIiLCAicG9zaXRpb24iOiB7IngiOiAxNi44NSwgInkiOiAtNS4zNSwgInlhdyI6IDMuMTR9LCAidGFncyI6IFtdfSwgeyJuYW1lIjogInAzIiwgInBvc2l0aW9uIjogeyJ4IjogMTQuOTUsICJ5IjogLTUuMTUsICJ5YXciOiAzLjE0fSwgInRhZ3MiOiBbXX0sIHsibmFtZSI6ICJwNCIsICJwb3NpdGlvbiI6IHsieCI6IDEyLjk1LCAieSI6IC01LjE1LCAieWF3IjogMy4xNH0sICJ0YWdzIjogW119LCB7Im5hbWUiOiAicDUiLCAicG9zaXRpb24iOiB7IngiOiAxMC45NSwgInkiOiAtNS4xNSwgInlhdyI6IDMuMTR9LCAidGFncyI6IFtdfSwgeyJuYW1lIjogInA2IiwgInBvc2l0aW9uIjogeyJ4IjogOC45NSwgInkiOiAtNS4xNSwgInlhdyI6IDMuMTR9LCAidGFncyI6IFtdfSwgeyJuYW1lIjogInA3IiwgInBvc2l0aW9uIjogeyJ4IjogNi45NSwgInkiOiAtNS4xNSwgInlhdyI6IDMuMTR9LCAidGFncyI6IFtdfSwgeyJuYW1lIjogInA4IiwgInBvc2l0aW9uIjogeyJ4IjogNC45NSwgInkiOiAtNS4xNSwgInlhdyI6IDMuMTR9LCAidGFncyI6IFtdfSwgeyJuYW1lIjogInA5IiwgInBvc2l0aW9uIjogeyJ4IjogMi45NSwgInkiOiAtNS4xNSwgInlhdyI6IDAuMH0sICJ0YWdzIjogW119LCB7Im5hbWUiOiAicDEwIiwgInBvc2l0aW9uIjogeyJ4IjogLTAuMTUsICJ5IjogLTQuODUsICJ5YXciOiAzLjE0fSwgInRhZ3MiOiBbXX0sIHsibmFtZSI6ICJwMTEiLCAicG9zaXRpb24iOiB7IngiOiAtMS41LCAieSI6IC0zLjA1LCAieWF3IjogMC4wfSwgInRhZ3MiOiBbXX0sIHsibmFtZSI6ICJwMTIiLCAicG9zaXRpb24iOiB7IngiOiAwLjksICJ5IjogLTIuOTUsICJ5YXciOiAzLjE0fSwgInRhZ3MiOiBbXX0sIHsibmFtZSI6ICJwMTMiLCAicG9zaXRpb24iOiB7IngiOiAwLjcsICJ5IjogLTAuMDUsICJ5YXciOiAzLjE0fSwgInRhZ3MiOiBbXX0sIHsibmFtZSI6ICJwMTQiLCAicG9zaXRpb24iOiB7IngiOiAtMS43NSwgInkiOiAtMC4wNSwgInlhdyI6IDAuMH0sICJ0YWdzIjogW119XSwgImNoYXJnZV9wb2ludHNfaW5mbyI6IFt7Im5hbWUiOiAiY2hhcmdlIiwgInBvc2l0aW9uIjogeyJ4IjogLTEyLjc0NDYsICJ5IjogOS4yMTc0MywgInlhdyI6IDAuMDE3NTA4MX19XSwgImdyb3VwcyI6IHsiIzEzXzA3XzE1XzAwIyI6IFtdLCAiIzE1XzMxXzE3XzAwIyI6IFtdLCAiIzA4XzU0XzEyXzAzIyI6IFtdLCAiIzE3XzEwXzIwXzAwIyI6IFtdLCAiI3JlZCMiOiBbInAxIiwgInAyIiwgInAzIiwgInA0IiwgInA1IiwgInA2IiwgInA3IiwgInA4IiwgInA5IiwgInAxMCIsICJwMTEiLCAicDEyIiwgInAxMyIsICJwMTQiXX19"
    print R.getBase64(b1)
    
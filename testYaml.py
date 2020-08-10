# -*- coding: utf-8 -*-
import io
import yaml
with open("conf/config2.yaml",'r') as yfile:
    try:
        # yobj = yaml.safe_load(yfile.read())
        yobj = yaml.safe_load(yfile)
        print yobj.get('goCharge')
        print yobj.get('robot_mac')
    except yaml.YAMLError as error:
        print error
# with open('conf/config2.yaml', 'w') as wfile:
#         yaml.dump(yobj, wfile, allow_unicode=True)

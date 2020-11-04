# -*- coding:utf-8 -*-
from ruamel import yaml
def setDictYaml(fileDir, key, value):
    with open(fileDir, 'r') as f:
        doc = yaml.round_trip_load(f)
    doc[key] = value
    with open(fileDir, 'w') as f:
        yaml.round_trip_dump(doc, f, default_flow_style=False)

def readYaml(fileDir):
    with open(fileDir, 'r') as ya:
        try:
            obj = yaml.safe_load(ya)
        except Exception as e:
            print (e)
        print (obj['password'][1])

# if __name__ == "__main__":

#     setDictYaml('../conf/test.yaml', 'password', [1,2,3])
#     readYaml('../conf/test.yaml')
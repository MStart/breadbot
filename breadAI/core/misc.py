from configobj import ConfigObj
import os
import re
import time


def init_input(inStr):
    inStr = inStr.lower()
    inStrList = list(inStr)
    rightLetters = 'abcdefghijklmnopqrstuvwxyz0123456789 '
    for i, chr in enumerate(inStrList):
        if chr in rightLetters:
            continue
        elif re.match(u'[\u4e00-\u9fa5]', chr):
            continue
        else:
            inStrList[i] = ' '
    inStr = ''.join(inStrList)
    inStr = re.sub(r'\s{2,}', ' ', inStr)
    inStr = re.sub(r'(^ +| +$)', '', inStr)
    return inStr


class log(object):
    def __init__(self):
        upDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.logDir = os.path.join(os.path.join(upDir, 'log'), 'dia.log')

    def write(self, inStr):
        curTime = time.strftime('[%Y-%m-%d %H:%M:%S] ', time.localtime())
        text = curTime + inStr
        f = open(self.logDir, 'a')
        f.write(text + '\n')
        f.close()
        return text

    def print(self, inStr):
        curTime = time.strftime('[%Y-%m-%d %H:%M:%S] ', time.localtime())
        print(curTime + str(inStr))


class cfg(object):
    def __init__(self):
        self.cfg = ConfigObj('/etc/bread.cfg')

    def get(self, value):
        if value == 'server_ip':
            return self.cfg['normal']['server_ip']
        elif value == 'data_path':
            return self.cfg['normal']['data_path']
        elif value == 'super_users':
            userList = []
            for user in self.cfg['super_users']:
                userList.append(self.cfg['super_users'][user])
            return userList

    def write(self, value, key):
        if value == 'server_ip':
            self.cfg['normal']['server_ip'] = key
        elif value == 'data_path':
            self.cfg['normal']['data_path'] = key
        self.cfg.write()

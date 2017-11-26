from configobj import ConfigObj
import os
import re
import time


def init_input(inStr):
    inStr = re.sub('\s', ' ', inStr)
    inStr = re.sub('  ', ' ', inStr)
    inStr = re.sub(r'(^ +| +$)', '', inStr)
    inStr = inStr.lower()
    return inStr


class log(object):
    def __init__(self):
        self.logDir = os.path.join(cfg().get('log_path'), 'dia.log')

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
        if value == 'token':
            return self.cfg['normal']['token']
        elif value == 'server_ip':
            return self.cfg['normal']['server_ip']
        elif value == 'data_path':
            return self.cfg['normal']['data_path']
        elif value == 'log_path':
            return self.cfg['normal']['log_path']
        elif value == 'super_users':
            userList = []
            for user in self.cfg['super_users']:
                userList.append(self.cfg['super_users'][user])
            return userList

    def write(self, value, key):
        if value == 'token':
            self.cfg['normal']['token'] = key
        elif value == 'server_ip':
            self.cfg['normal']['server_ip'] = key
        elif value == 'data_path':
            self.cfg['normal']['data_path'] = key
        elif value == 'log_path':
            self.cfg['normal']['log_path'] = key
        self.cfg.write()

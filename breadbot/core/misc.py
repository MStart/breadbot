from configobj import ConfigObj
import os
import re
import time


def init_input(inStr):
    inStr = re.sub('\s', ' ', inStr)
    inStr = re.sub('  ', ' ', inStr)
    inStr = re.sub(r'(^ +| +$)', '', inStr)
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
        if value == 'data_path':
            return self.cfg['local']['data_path'].split(':')
        elif value == 'log_path':
            return self.cfg['local']['log_path']
        elif value == 'token':
            return self.cfg['wechat']['token']
        elif value == 'server_ip':
            return self.cfg['wechat']['server_ip']
        elif value == 'super_user':
            return self.cfg['wechat']['super_user'].split(':')
        elif value == 'db_name':
            return self.cfg['mongodb']['db_name']
        elif value == 'db_ip':
            return self.cfg['mongodb']['db_ip']
        elif value == 'db_port':
            return int(self.cfg['mongodb']['db_port'])

    def write(self, value, key):
        if value == 'data_path':
            if type(key) != list:
                raise Exception("data_path must be a list")
            self.cfg['local']['data_path'] = ':'.join(key)
        elif value == 'log_path':
            self.cfg['local']['log_path'] = key
        elif value == 'token':
            self.cfg['wechat']['token'] = key
        elif value == 'server_ip':
            self.cfg['wechat']['server_ip'] = key
        elif value == 'super_user':
            if type(key) != list:
                raise Exception("super_user must be a list")
            self.cfg['wechat']['super_user'] = ':'.join(key)
        self.cfg.write()

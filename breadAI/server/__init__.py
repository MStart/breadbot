from . import manage
from . import server
from . import wechat
import os
from breadAI import core

def start():
    ma_path = manage.__file__
    ip = core.misc.get_cfg()['normal']['server_ip']
    port = '80'
    exeList = ['python3', ma_path, 'runserver', ':'.join([ip, port])]
    exeStr = ' '.join(exeList)
    os.system(exeStr)

from . import manage
from . import server
from . import wechat
import os
import re
import sys
from breadAI import core

def start():
    ma_path = manage.__file__
    ip = core.misc.get_cfg()['normal']['server_ip']
    if not re.match(r"^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$", ip):
        print('Error: Please configure your server ip on /etc/bread.cfg')
        sys.exit(1)
    port = '80'
    exeList = ['python3', ma_path, 'runserver', ':'.join([ip, port])]
    exeStr = ' '.join(exeList)
    os.system(exeStr)

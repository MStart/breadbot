import os
import re
import sys

from . import manage
from breadAI import core


def start():
    ma_path = manage.__file__
    ip = core.misc.get_cfg('server_ip')
    if not re.match(r"^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}"
                    r"(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$", ip):
        cmd = input('Error: Please enter your server ip: ')
        core.misc.write_cfg('server_ip', cmd)
    port = '80'
    exeList = ['python3', ma_path, 'runserver', ':'.join([ip, port])]
    exeStr = ' '.join(exeList)
    os.system(exeStr)

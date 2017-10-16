import os
import re
import sys

from breadAI.core import misc
from . import manage


def start():
    ma_path = manage.__file__
    ip = misc.cfg().get('server_ip')
    if not re.match(r"^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}"
                    r"(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$", ip):
        ip = input('Error: Please enter your server ip: ')
        misc.cfg().write('server_ip', ip)
    port = '80'
    exeList = ['python3', ma_path, 'runserver', ':'.join([ip, port])]
    exeStr = ' '.join(exeList)
    os.system(exeStr)

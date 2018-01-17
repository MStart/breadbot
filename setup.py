#!/usr/bin/python3
import os
import sys
from setuptools import setup

from breadbot import core


if len(sys.argv) <= 1:
    print('Please enter install, uninstall or clean')
    sys.exit(1)

elif sys.argv[1] == 'install':
    os.system('pip3 install -U pip')
    os.system('pip3 install -r requirements.txt')
    setup(
        setup_requires=['pbr>=0.1'],
        pbr=True,)
    data_path = [os.path.join(os.getcwd(), 'data')]
    core.misc.cfg().write('data_path', data_path)
    os.system('breadbot import')

elif sys.argv[1] == 'uninstall':
    core.data.Data().drop_db()
    os.system('pip3 uninstall breadbot')
    os.system('rm -f /etc/bread.cfg')
    os.system('rm -f /usr/local/bin/breadbot')
    sys.exit(0)

elif sys.argv[1] == 'clean':
    exclude = [
        '.git',
        '.gitignore',
        '.tox',
        'bin',
        'breadbot',
        'data',
        'etc',
        'log',
        'tests',
        'tools',
        'LICENSE',
        'NEWS',
        'README.md',
        'requirements.txt',
        'setup.cfg',
        'setup.py',
        'tox.ini',
    ]
    fileList = os.listdir('.')
    for f in fileList:
        if f not in exclude:
            os.system('rm -rf %s' % f)
    os.system('find -name "__pycache__"|xargs rm -rf')
    sys.exit(0)

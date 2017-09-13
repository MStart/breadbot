#!/usr/bin/python3
import os
import subprocess
import sys
from setuptools import setup


if len(sys.argv) <= 1:
    print('Please enter install or uninstall')
    sys.exit(1)

elif sys.argv[1] == 'install':
    subprocess.Popen('pip3 install -r requirements.txt')
    setup(
        setup_requires=['pbr>=0.1'],
        pbr=True,)
    from breadAI import core
    core.data.insertData()

elif sys.argv[1] == 'uninstall':
    subprocess.Popen('pip3 uninstall breadAI', shell=True)
    subprocess.Popen('rm -f /etc/bread.cfg', shell=True)
    subprocess.Popen('rm -f /usr/bin/bread-console', shell=True)
    subprocess.Popen('rm -rf /usr/share/breadAI', shell=True)
    sys.exit(0)

elif sys.argv[1] == 'clean':
    saveList = [
        'bin',
        'breadAI',
        'data',
        'etc',
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
        if f[0] == '.':
            continue
        elif f not in saveList:
            subprocess.Popen('rm -rf %s' % f, shell=True)
    subprocess.Popen('find -name "__pycache__"|xargs rm -rf', shell=True)
    sys.exit(0)

else:
    setup(
        setup_requires=['pbr>=0.1'],
        pbr=True,)

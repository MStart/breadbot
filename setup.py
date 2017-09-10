#!/usr/bin/python3
from setuptools import setup
import sys
import os

if len(sys.argv) <= 1:
    print('Please enter install or uninstall')
    sys.exit(1)

elif sys.argv[1] == 'install':
    os.system('pip3 install -r requirements.txt')
    setup(
        setup_requires=['pbr>=0.1'],
        pbr=True,)
    from breadAI import core
    data_dir = core.misc.get_cfg()['normal']['data_dir']
    db_dir = os.path.join(data_dir, 'data.db')
    if not os.path.exists(db_dir):
        core.data.insertData()

elif sys.argv[1] == 'uninstall':
    os.system('pip3 uninstall breadAI')
    os.system('rm -f /etc/bread.cfg')
    os.system('rm -f /usr/bin/bread-console')
    os.system('rm -rf /usr/share/breadAI')
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
    ]
    fileList = os.listdir('.')
    for f in fileList:
        if f[0] == '.':
            continue
        elif f not in saveList:
            os.system('rm -rf '+f)
    os.system('find -name "__pycache__"|xargs rm -rf')
    sys.exit(0)

else:
    print('Nothing happend')
    sys.exit(1)

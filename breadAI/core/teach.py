import os

from . import data
from . import misc


def response(inStr, isSuper=False):
    if not isSuper:
        return
    if not inStr:
        return
    if '//' not in inStr:
        return
    data_path = misc.cfg().get('data_path')
    file_path = os.path.join(data_path, 'dia/new.yml')
    f = open(file_path, 'a')
    que = inStr.split('//')[0]
    ans = inStr.split('//')[1]
    text = '\n- que:\n  - %s\n  ans:\n  - %s\n' % (que, ans)
    f.write(text)
    f.close()
    data.insertData()
    return 'OK, I learn.'

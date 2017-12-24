import os

from . import data
from . import misc


def response(inStr, isSuper=False):
    splitSignal = '//'
    if not isSuper:
        return
    if not inStr:
        return
    if splitSignal not in inStr:
        return
    data_path = misc.cfg().get('data_path')
    file_path = os.path.join(data_path, 'new.yml')
    f = open(file_path, 'a')
    que = inStr.split(splitSignal)[0]
    ans = inStr.split(splitSignal)[1]
    text = '\n- que:\n  - %s\n  ans:\n  - %s\n' % (que, ans)
    f.write(text)
    f.close()
    data.insertData()
    return 'OK, I learned.'

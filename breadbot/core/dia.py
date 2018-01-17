import random
import re
import string

from breadbot.core import misc


def response(db, user, inStr):
    inStr = misc.expand_abbrev(inStr)
    inStr = re.sub('[%s]+' % string.punctuation, '', inStr)
    inStr = inStr.lower()
    res = []
    colls = db.collection_names()
    for coll in colls:
        if coll[-4:] != '_yml':
            continue
        reqs = db[coll].find_one()
        tags = reqs['tag']
        if 'dia' not in tags:
            continue
        qas = reqs['QA']
        if not qas:
            continue
        for qa in qas:
            ques = qa['que']
            if inStr in ques:
                ans = qa['ans']
                if type(ans) is not list:
                    ans = [ans]
                res += ans
    if res:
        res = random.choice(res)
    return res

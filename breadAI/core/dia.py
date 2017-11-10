import random


def response(db, inStr, isSuper=False):
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
                res += qa['ans']
    if res:
        res = random.choice(res)
    return res

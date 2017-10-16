import random


def response(db, inStr, isSuper=False):
    res = '...'
    colls = db.collection_names()
    for coll in colls:
        if coll == 'system.indexes':
            continue
        reqs = db[coll].find_one()
        tags = reqs['tag']
        if 'nom' in tags:
            continue
        elif 'sec' in tags and not isSuper:
            continue
        qas = reqs['QA']
        for qa in qas:
            ques = qa['que']
            if inStr in ques:
                res = qa['ans']
                break
    if type(res) == list:
        res = random.choice(res)
    return res

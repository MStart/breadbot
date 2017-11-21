import random
import re

from breadAI.core import memo

firstLine = 'Do you mean:'


def _get_qas(db, coll, isSuper=False):
    if coll[-4:] != '_yml':
        return
    reqs = db[coll].find_one()
    tags = reqs['tag']
    if 'dia' in tags:
        return
    elif 'sec' in tags and not isSuper:
        return
    qas = reqs['QA']
    return qas


def response(db, inStr, isSuper=False):
    regexStr = '(^|.* )' + inStr + '( .*|$)'
    colls = db.collection_names()
    dias = memo.dialogue().get_dia()
    lastDia = {}
    lastAns = []
    if dias:
        lastDia = dias[-1]
    if lastDia:
        lastAns = list(lastDia.values())[0]
    newQues = []
    if firstLine in lastAns:
        ques = lastAns.split('\n')[1:]
        for que in ques:
            if re.match(regexStr, que):
                newQues.append(que)
    newQues = list(set(newQues))
    if len(newQues) < 1:
        for coll in colls:
            qas = _get_qas(db, coll, isSuper)
            if not qas:
                continue
            for qa in qas:
                ques = qa['que']
                for que in ques:
                    if re.match(regexStr, que):
                        newQues.append('- ' + que)
                        break
    if len(newQues) < 1:
        words = inStr.split(' ')
        for coll in colls:
            qas = _get_qas(db, coll, isSuper)
            if not qas:
                continue
            for qa in qas:
                ques = qa['que']
                for que in ques:
                    all_words_in = True
                    que_words = que.split(' ')
                    for word in words:
                        if word not in que_words:
                            all_words_in = False
                            break
                    if all_words_in:
                        newQues.append('- ' + que)
    if len(newQues) < 1:
        res = None
    elif len(newQues) == 1:
        Que = newQues[0]
        Que = re.sub(r'^- ', '', Que)
        for coll in colls:
            qas = _get_qas(db, coll, isSuper)
            if not qas:
                continue
            for qa in qas:
                ques = qa['que']
                if Que in ques:
                    res = qa['ans']
                    break
        if type(res) == list:
            res = random.choice(res)
        if res[-1] == '\n':
            res = res[:-1]
        if res[:2] != '- ':
            res = '- ' + res
        res = Que + '?\n' + res
    else:
        newQues.insert(0, firstLine)
        res = '\n'.join(newQues)
    if res:
        memo.dialogue().insert_dia(inStr, res)
    return res

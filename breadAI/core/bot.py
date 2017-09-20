# This is the bot function of Bread
import os
import pydblite
import random
import re
import sys

from . import memory
from . import misc
import breadAI


class brain(object):

    def __init__(self):
        self.dontKnow = "I don't know."
        dataDir = os.path.dirname(breadAI.data.__file__)
        dbDir = os.path.join(dataDir, 'data.db')
        self.db = self.open_db(dbDir)

    def open_db(self, dbDir):
        db = pydblite.Base(dbDir)
        if db.exists():
            db.open()
            return db
        else:
            print('[Error] No database found')
            sys.exit(1)

    def init_input(self, inStr):
        inStr = inStr.lower()
        inStrList = list(inStr)
        rightLetters = 'abcdefghijklmnopqrstuvwxyz0123456789 '
        for i, letter in enumerate(inStrList):
            if letter in rightLetters:
                continue
            else:
                inStrList[i] = ' '
        inStr = ''.join(inStrList)
        inStr = re.sub(r'\s{2,}', ' ', inStr)
        inStr = re.sub(r'(^ +| +$)', '', inStr)
        return inStr

    def search_que(self, inStr, isSuper=False):
        inStr = self.init_input(inStr)
        regexStr = '(^|.* )' + inStr + '( .*|$)'
        firstLine = 'Do you mean:'
        diaList = memory.dialogueMem().get_dia()
        newList = []
        if firstLine in diaList[-1]:
            queList = diaList[-1].split('\n')[1:]
            for que in queList:
                if re.match(regexStr, que):
                    newList.append(que)
        else:
            for item in self.db:
                tag = item['tag']
                if tag == 'dia':
                    continue
                elif tag == 'sec' and not isSuper:
                    continue
                que = item['question']
                if re.match(regexStr, que):
                    newList.append('- ' + que)
        if len(newList) < 1:
            res = None
        elif len(newList) == 1:
            que = newList[0]
            que = re.sub(r'^- ', '', que)
            res = self.db(question=que)[0]['answer']
            if type(res) == list:
                res = random.choice(res)
            res = que + '?\n' + res
        else:
            newList.insert(0, firstLine)
            res = '\n'.join(newList)
        return res

    def response(self, inStr, isSuper=False):
        inStr = self.init_input(inStr)
        res = self.db(question=inStr, tag='nom')
        if not res and isSuper:
            res = self.db(question=inStr, tag='sec')
        if not res:
            res = self.search_que(inStr, isSuper)
        if not res:
            res = self.db(question=inStr, tag='dia')
        if not res:
            res = self.dontKnow
        else:
            if type(res) is list:
                res = random.choice(res)
            if type(res) is not str:
                res = res['answer']
            memory.dialogueMem().insert_dia(res)
        return res


class chat(object):

    def __init__(self):
        self.bot = brain()

    def response(self, inStr, isSuper=False):
        if re.match(u'^s .*$', inStr):
            content = re.sub(u'^s ', '', inStr)
            if not len(content):
                res = '[Not Found]'
            else:
                res = misc.translate(content)
        elif re.match(u'^d .*$', inStr):
            content = re.sub(u'^d ', '', inStr)
            if not len(content):
                res = '[Not Found]'
            else:
                res = misc.baiduSearch(content)
        elif re.match(u'^w .*$', inStr):
            content = re.sub(u'^w ', '', inStr)
            if not len(content):
                res = '[Not Found]'
            else:
                res = misc.wikiSearch(content)
        elif re.match(u'^(n|next)$', inStr):
            res = memory.longStr().read_mem()
        else:
            for s in inStr:
                if re.match(u'[\u4e00-\u9fa5]', s):
                    return 'I speak English only'
            res = self.bot.response(inStr, isSuper)
        res = memory.longStr().check_long_str(res)
        return res

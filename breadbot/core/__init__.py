import os
import pydblite
import random
import re
import sys
from pymongo import MongoClient

from . import data
from . import dia
from . import klg
from . import memo
from . import misc
from . import search
from . import teach


class chat(object):

    def __init__(self):
        self.dontKnow = "I don't know."
        self.db = self.open_db('breadDB')

    def open_db(self, dbName):
        client = MongoClient('localhost', 27017)
        db = client[dbName]
        return db

    def response(self, inStr, isSuper=False):
        if "'" in inStr:
            return 'Please do not use \''
        inStr = misc.init_input(inStr)

        if re.match('^(n|next)$', inStr):
            res = memo.longStr().read_mem()
        elif re.match('^s .*$', inStr):
            content = re.sub('^s ', '', inStr)
            res = search.translate(content)
        elif re.match('^d .*$', inStr):
            content = re.sub('^d ', '', inStr)
            res = search.baiduSearch(content)
        elif re.match('^w .*$', inStr):
            content = re.sub('^w ', '', inStr)
            res = search.wikiSearch(content)
        elif re.match('^t .*$', inStr):
            content = re.sub('^t ', '', inStr)
            res = teach.response(content, isSuper)
        elif re.search('[\u4e00-\u9fa5]', inStr):
            return 'I speak English only'
        else:
            que = ''
            ans = ''
            lastDia = {}
            lastDias = memo.dialogue().get_dia()
            if lastDias:
                lastDia = lastDias[-1]
                que = list(lastDia.keys())[0]
                ans = list(lastDia.values())[0]
            if inStr == que or klg.do_you_mean in ans:
                res = klg.response(self.db, inStr, isSuper)
                if not res:
                    res = dia.response(self.db, inStr, isSuper)
            else:
                res = dia.response(self.db, inStr, isSuper)
                if not res:
                    res = klg.response(self.db, inStr, isSuper)
        if not res:
            notList = [
                'Sorry, I dont understand',
                'What are you saying?',
                'Hey, let us change a topic ok?',
                'I dont know clearly',
                'Let us say something others']
            res = random.choice(notList)
        memo.dialogue().insert_dia(inStr, res)
        res = memo.longStr().check_long_str(res)
        return res

import os
import pydblite
import random
import re
import sys
from pymongo import MongoClient

from . import memo
from . import misc
from . import data
from . import memo
from . import misc
from . import search
from . import dia
from . import nom


class chat(object):

    def __init__(self):
        self.dontKnow = "I don't know."
        self.db = self.open_db('breadDB')

    def open_db(self, dbName):
        client = MongoClient('localhost', 27017)
        db = client[dbName]
        return db

    def response(self, inStr, isSuper=False):
        inStr = misc.init_input(inStr)
        res = '...'

        if re.match('^(n|next)$', inStr):
            res = memo.longStr().read_mem()
        elif re.match('^s .*$', inStr):
            content = re.sub('^s ', '', inStr)
            if not len(content):
                res = '[Not Found]'
            else:
                res = search.translate(content)
        elif re.match('^d .*$', inStr):
            content = re.sub('^d ', '', inStr)
            if not len(content):
                res = '[Not Found]'
            else:
                res = search.baiduSearch(content)
        elif re.match('^w .*$', inStr):
            content = re.sub('^w ', '', inStr)
            if not len(content):
                res = '[Not Found]'
            else:
                res = search.wikiSearch(content)
        else:
            for chr in inStr:
                if re.match('[\u4e00-\u9fa5]', chr):
                    return 'I speak English only'
            res = nom.response(self.db, inStr, isSuper)
            if not res:
                res = dia.response(self.db, inStr, isSuper)
        memo.dialogue().insert_dia(res)
        res = memo.longStr().check_long_str(res)
        return res

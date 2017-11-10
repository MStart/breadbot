import os
import pydblite
import random
import re
import sys
from pymongo import MongoClient

from . import data
from . import dia
from . import memo
from . import misc
from . import nom
from . import search


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
            res = 'Please do not use \''
            return res
        elif re.search('[\u4e00-\u9fa5]', inStr):
            res = 'I speak English only'
            return res
        inStr = misc.init_input(inStr)

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
            lastDia = ''
            lastDias = memo.dialogue().get_dia()
            if lastDias:
                lastDia = lastDias[-1]
            if inStr in lastDia.keys():
                res = nom.response(self.db, inStr, isSuper)
                if not res:
                    res = dia.response(self.db, inStr, isSuper)
            else:
                res = dia.response(self.db, inStr, isSuper)
                if not res:
                    res = nom.response(self.db, inStr, isSuper)
        if not res:
            res = '...'
        memo.dialogue().insert_dia(inStr, res)
        res = memo.longStr().check_long_str(res)
        return res

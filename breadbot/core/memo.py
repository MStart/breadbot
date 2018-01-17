import os
from pymongo import MongoClient
import re

from . import misc

MEM_COLL = 'breadbot_memory_'


def get_mem_coll(user):
    db_name = misc.cfg().get('db_name')
    ip = misc.cfg().get('db_ip')
    port = misc.cfg().get('db_port')
    client = MongoClient(ip, port)
    db = client[db_name]
    colls = db.collection_names()
    mem_coll = '%s%s' % (MEM_COLL, user)
    coll = db[mem_coll]
    if mem_coll not in colls or not coll.find_one():
        data = {
            'dialogue': [],
            'long_str': {
                'cur_block': 0,
                'block_count': 0,
                'content': []
            }
        }
        coll.insert(data)
    return coll


def insert_to_coll(coll, data):
    coll.remove({})
    coll.insert(data)


class longStr(object):

    def __init__(self, user):
        self.maxWords = 140
        self.nextSymble = r'....'
        self.mem_coll = get_mem_coll(user)
        self.mem_data = self.mem_coll.find_one()

    def _split_str(self, text):
        blockCount = len(text) // self.maxWords
        if len(text) % self.maxWords != 0:
            blockCount += 1
        self.mem_data['long_str']['block_count'] = blockCount
        self.mem_data['long_str']['cur_block'] = 1
        text = text.encode('unicode-escape').decode()
        content = [
            text[i:i + self.maxWords]
            for i in range(0, len(text), self.maxWords)]
        self.mem_data['long_str']['content'] = content
        insert_to_coll(self.mem_coll, self.mem_data)

    def read_mem(self):
        textList = self.mem_data['long_str']['content']
        curBlock = int(self.mem_data['long_str']['cur_block'])
        blockCount = int(self.mem_data['long_str']['block_count'])
        if curBlock <= blockCount and textList:
            res = textList[curBlock - 1] + self.nextSymble
            self.mem_data['long_str']['cur_block'] = str(curBlock + 1)
            insert_to_coll(self.mem_coll, self.mem_data)
            if curBlock == blockCount:
                res = res.replace(self.nextSymble, '')
        else:
            res = 'no more'
        res = res.replace(r'\n', '\n')
        res = res.replace(r'\r', '\r')
        return res

    def check_long_str(self, text):
        if len(text) <= self.maxWords or self.nextSymble in text:
            return text
        elif 'http://' in text or 'https://' in text:
            return text
        elif re.match(u'[\u4e00-\u9fa5]+', text):
            return text
        else:
            self._split_str(text)
            return self.read_mem()


class dialogue(object):

    def __init__(self, user):
        self.maxLen = 3
        self.mem_coll = get_mem_coll(user)
        self.mem_data = self.mem_coll.find_one()

    def insert_dia(self, inStr, res):
        if inStr == 'n' or inStr == 'next':
            return
        diaList = self.mem_data['dialogue']
        if len(diaList) >= self.maxLen:
            diaList.pop(0)
        inStr = inStr.encode('unicode-escape').decode()
        res = res.encode('unicode-escape').decode()
        diaList.append({inStr: res})
        self.mem_data['dialogue'] = diaList
        insert_to_coll(self.mem_coll, self.mem_data)

    def get_dia(self):
        dias = self.mem_data['dialogue']
        if not dias:
            return []
        newDias = []
        for dia in dias:
            newDias.append(dia)
        return newDias

    def erase_dia(self):
        self.mem_data['dialogue'] = []
        insert_to_coll(self.mem_coll, self.mem_data)

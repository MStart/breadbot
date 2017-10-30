from configobj import ConfigObj
import os
import re

from . import misc


class longStr(object):

    def __init__(self):
        self.maxWords = 140
        self.nextSignal = r'....'
        self.splitSignal = r'///'
        memPath = self.get_mem_path()
        self.mem = ConfigObj(memPath)
        self.memLS = self.mem['long_str']

    def get_mem_path(self):
        memPath = os.path.join(misc.cfg().get('log_path'), 'mem.log')
        return memPath

    def split_str(self, text):
        blockCount = len(text) // self.maxWords
        if len(text) % self.maxWords != 0:
            blockCount += 1
        curBlock = 1
        self.memLS['cur_block'] = str(curBlock)
        self.memLS['block_count'] = str(blockCount)
        self.memLS['content'] = self.splitSignal.join(
            [text[i:i + self.maxWords]
             for i in range(0, len(text), self.maxWords)])
        self.mem.write()

    def check_long_str(self, text):
        if len(text) <= self.maxWords or self.nextSignal in text:
            return text
        elif 'http://' in text or 'https://' in text:
            return text
        elif re.match(u'[\u4e00-\u9fa5]+', text):
            return text
        else:
            self.split_str(text)
            return self.read_mem()

    def read_mem(self):
        textList = self.memLS['content'].split(self.splitSignal)
        curBlock = int(self.memLS['cur_block'])
        blockCount = int(self.memLS['block_count'])
        if curBlock <= blockCount:
            res = textList[curBlock - 1] + self.nextSignal
            self.memLS['cur_block'] = str(curBlock + 1)
            self.mem.write()
            if curBlock == blockCount:
                res = res.replace(self.nextSignal, '')
        else:
            res = 'no more'
        res = res.replace(self.splitSignal, '')
        return res


class dialogue(object):

    def __init__(self):
        self.maxLen = 3
        self.splitSignal = r'///'
        memPath = self.get_mem_path()
        self.mem = ConfigObj(memPath)
        self.memDia = self.mem['dialogue']

    def get_mem_path(self):
        upPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        memPath = os.path.join(os.path.join(upPath, 'log'), 'mem.log')
        return memPath

    def insert_dia(self, dia):
        if dia == 'n' or dia == 'next':
            return None
        diaList = self.memDia['content'].split(self.splitSignal)
        if len(diaList) >= self.maxLen:
            diaList.pop(0)
        diaList.append(dia)
        self.memDia['content'] = str(self.splitSignal.join(diaList))
        self.mem.write()

    def get_dia(self):
        return self.memDia['content'].split(self.splitSignal)

    def erase_dia(self):
        self.memDia['content'] = ''
        self.mem.write()

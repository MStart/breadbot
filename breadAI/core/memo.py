from configobj import ConfigObj
import os
import re

from . import misc


class longStr(object):

    def __init__(self):
        self.maxWords = 140
        self.nextSignal = r'....'
        self.spSignal = r'///'
        memPath = self._get_mem_path()
        self.mem = ConfigObj(memPath)
        self.memLS = self.mem['long_str']

    def _get_mem_path(self):
        memPath = os.path.join(misc.cfg().get('log_path'), 'mem.log')
        return memPath

    def split_str(self, text):
        blockCount = len(text) // self.maxWords
        if len(text) % self.maxWords != 0:
            blockCount += 1
        curBlock = 1
        self.memLS['cur_block'] = str(curBlock)
        self.memLS['block_count'] = str(blockCount)
        self.memLS['content'] = self.spSignal.join(
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
        textList = self.memLS['content'].split(self.spSignal)
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
        res = res.replace(self.spSignal, '')
        return res


class dialogue(object):

    def __init__(self):
        self.maxLen = 3
        self.spSignal = '//'
        self.spSignal2 = '///\n'
        memPath = self._get_mem_path()
        self.mem = ConfigObj(memPath)
        self.memDia = self.mem['dialogue']

    def _get_mem_path(self):
        upPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        memPath = os.path.join(os.path.join(upPath, 'log'), 'mem.log')
        return memPath

    def insert_dia(self, inStr, res):
        if inStr == 'n' or inStr == 'next':
            return
        diaList = self.memDia['content'].split(self.spSignal2)
        if len(diaList) >= self.maxLen:
            diaList.pop(0)
        diaList.append(str(inStr.encode()) + self.spSignal + res)
        self.memDia['content'] = str(self.spSignal2.join(diaList))
        self.mem.write()

    def get_dia(self):
        dias = self.memDia['content'].split(self.spSignal2)
        if not dias:
            return []
        newDias = []
        for dia in dias:
            qa = dia.split(self.spSignal)
            if len(qa) == 2:
                q = qa[0]
                a = qa[1]
                newDias.append({q: a})
        return newDias

    def erase_dia(self):
        self.memDia['content'] = ''
        self.mem.write()

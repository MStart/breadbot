from configobj import ConfigObj
import os
import re


class longStr(object):

    def __init__(self):
        self.maxWords = 140
        self.nextSignal = r'....'
        self.splitSignal = '///'
        memDir = self.get_mem_dir()
        self.mem = ConfigObj(memDir)
        self.memLS = self.mem['long_str']

    def get_mem_dir(self):
        curDir = os.path.dirname(__file__)
        memDir = os.path.join(curDir, 'mem.txt')
        return memDir

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
        if len(textList) > 0:
            curBlock = int(self.memLS['cur_block'])
            blockCount = int(self.memLS['block_count'])
            if curBlock < blockCount:
                res = textList[curBlock + 1] + self.nextSignal
                self.memLS['cur_block'] = str(curBlock + 1)
                self.memLS['content'] = self.splitSignal.join(textList)
                self.mem.write()
            elif curBlock == blockCount:
                res = textList[curBlock + 1]
        else:
            res = 'no more'
        return res.replace(self.splitSignal, '')

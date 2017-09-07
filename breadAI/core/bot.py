# This is the bot function of Bread
import os
import sys
import re
import pydblite
import random
from . import misc

class whiteBoard(object):

    def __init__(self):
        self.maxWords = 140
        self.wbDir = self.get_wb_dir()
        self.nextSignal = r'....'
        self.splitSignal = '\n\n'

    def get_wb_dir(self):
        curDir = os.path.dirname(__file__)
        wbDir = os.path.join(curDir, 'wb.txt')
        return wbDir

    def erase_wb(self):
        wb = open(self.wbDir,'w')
        wb.close()
    
    def split_str(self,text):
        all_blocks = len(text) // self.maxWords
        if len(text) % self.maxWords != 0:
            all_blocks += 1
        current_block = 1
        wb = open(self.wbDir,'w')
        wb.writelines([str(all_blocks)+self.splitSignal, str(current_block)+self.splitSignal])
        wb.writelines([text[i:i+self.maxWords]+self.splitSignal for i in range(0,len(text),self.maxWords)])
        wb.close()

    def check_large_str(self,text):
        if len(text) <= self.maxWords or self.nextSignal in text:
            return text
        elif 'http://' in text or 'https://' in text:
            return text
        elif re.match(u'[\u4e00-\u9fa5]+', text):
            return text
        else:
            self.split_str(text)
            return self.read_wb()

    def read_wb(self):
        rb = open(self.wbDir,'r')
        list = rb.read().split(self.splitSignal)
        for i in range(len(list)):
            if list[i] == '' or list[i] == '\n':
                del list[i]
                continue
            list[i] += self.splitSignal
        rb.close()
        if len(list) > 2:
            all_blocks = int(list[0].replace(self.splitSignal,''))
            current_block = int(list[1].replace(self.splitSignal,''))
            if current_block < all_blocks:
                res = list[current_block+1] + self.nextSignal
                list[1] = str(current_block+1)+self.splitSignal
                wb = open(self.wbDir,'w')
                wb.writelines(list)
                wb.close()
            elif current_block == all_blocks:
                res = list[current_block+1]
                self.erase_wb()
        else:
            res = 'no more'
        return res.replace(self.splitSignal,'')

class brain(object):

    def __init__(self):
        dataDir = misc.get_cfg()['normal']['data_dir']
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
        inStr = re.sub(r'\s{2,}',' ',inStr)
        inStr = re.sub(r'(^ +| +$)','',inStr)
        return inStr

    def search_nom_que(self, inStr, isSuper=False):
        inStr = self.init_input(inStr)
        regexStr = '(^|.* )' + inStr + '( .*|$)'
        res = 'Do you mean: \n'
        for item in self.db:
            tag = item['tag']
            if tag == 'dia':
                continue
            elif tag == 'sec' and not isSuper:
                continue
            que = item['question']
            if re.match(regexStr, que):
                res += '- ' + que + '\n'
        res = res[:-1]
        if not '\n' in res:
            return None
        else:
            return res

    def response(self, inStr, isSuper=False):
        inStr = self.init_input(inStr)
        res = self.db(question=inStr)
        if not res:
            return None
        elif res[0]['tag'] == 'sec' and not isSuper:
            return None
        else:
            res = res[0]['answer']
            if type(res) == list:
                res = random.choice(res)
            return res

class chat(object):

    def __init__(self):
        self.bot = brain()
        self.dontKnow = "I don't know."

    def response(self, inStr, isSuper=False):
        if re.match(u'^s .*$', inStr):
            content = re.sub(u'^s ','',inStr)
            if not len(content):
                res = '[Not Found]'
            else:
                res = misc.translate(content)
        elif re.match(u'^d .*$', inStr):
            content = re.sub(u'^d ','',inStr)
            if not len(content):
                res = '[Not Found]'
            else:
                res = misc.baiduSearch(content)
        elif re.match(u'^(n|next)$', inStr):
            res = whiteBoard().read_wb()
        elif re.match(u'^search .*$', inStr):
            content = re.sub(u'^search ','',inStr)
            if not len(content):
                res = '[Not Found]'
            else:
                res = self.bot.search_nom_que(content, isSuper)
        else:
            for s in inStr:
                if re.match(u'[\u4e00-\u9fa5]', s):
                    return 'I speak English only'
            res = self.bot.response(inStr, isSuper)
        if not res:
            res = self.dontKnow
        res = whiteBoard().check_large_str(res)
        return res


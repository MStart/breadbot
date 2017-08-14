#!/usr/bin/env python3
import os
import sys
import re
import yaml
import pydblite
import re

class insertData():
    
    def __init__(self):
        dbDir = os.path.join(os.getcwd(), 'data.db')
        self.db = self.create_db(dbDir)
        self.dataFolder = os.path.join(os.getcwd(), 'yaml')
        self.fileInfoDir = os.path.join(os.getcwd(), 'file.ini')
        self.curFileInfoList = self.get_cur_data_file_list()
        self.oldFileInfoList = self.get_old_data_file_list()
        self.changedFileList = self.get_changed_file_list(self.curFileInfoList, self.oldFileInfoList)
        self.clean_old_data()
        self.insert_data()
        print('\n All Complete!')

    def create_db(self, dbDir):
        db = pydblite.Base(dbDir)
        if db.exists():
            db.open()
        else:
            db.create('file', 'tag', 'question', 'answer')
        return db

    def get_cur_data_file_list(self):
        curFileInfoList = []
        for root, dirs, files in os.walk(self.dataFolder):
            for file in files:
                if not re.match(r'^.*\.yml$', file):
                    continue
                fileDir = os.path.join(root, file)
                mtime = os.stat(fileDir).st_mtime
                info = ' '.join([fileDir, str(mtime)])
                curFileInfoList.append(info)
        return curFileInfoList

    def get_old_data_file_list(self):
        if os.path.exists(self.fileInfoDir):
            f = open(self.fileInfoDir, 'r')
            oldFileInfoList = f.readlines()
            for i in range(len(oldFileInfoList)):
                oldFileInfoList[i] = oldFileInfoList[i].replace('\n','')
            f.close()
            return oldFileInfoList
        else:
            f = open(self.fileInfoDir, 'w')
            f.close()
            return []

    def get_changed_file_list(self, curFileInfoList, oldFileInfoList):
        changedFileList = []
        for info in curFileInfoList:
            if not info in oldFileInfoList:
                changedFileList.append(info)
        return changedFileList

    def save_data_file_info(self, fileInfoList):
        f = open(self.fileInfoDir, 'w')
        for info in fileInfoList:
            f.write(info +'\n')
        f.close()

    def read_data(self, info):
        fileDir = info.split(' ')[0]
        oData = open(fileDir, 'r')
        readStr = oData.read()
        oData.close()
        readStr = re.sub(r'\n +\n', '\n\n', readStr)
        nData = readStr.split('\n\n')
        return nData

    def clean_old_data(self):
        print('cleaning database...')
        oldList = []
        for item in self.db:
            fileDir = item['file']
            changedFileStr = str(self.changedFileList)
            if fileDir in changedFileStr:
                oldList.append(item)
        if oldList:
            self.db.delete(oldList)

    def insert_data(self):
        for info in self.changedFileList:
            fileDir = info.split(' ')[0].replace(os.getcwd(), '')
            oData = self.read_data(info)
            nData = []
            tag = ''
            for od in oData:
                nd = yaml.load(od)
                if not nd: continue
                if 'tag' in nd.keys():
                    tag = nd['tag']
                else:
                    nData.append(nd)
            if not tag:
                print('[Error] No tag in %s' % fileDir)
                sys.exit(1)
            for nd in nData:
                print('\n[%s]\n%s' % (fileDir, nd))
                for que in nd['que']:
                    ans = nd['ans']
                    if type(que) == bool or type(ans) == bool:
                        print('\n[Error] Bool value\n[%s]\n%s' % (fileDir, nd))
                        self.save_data_file_info(self.curFileInfoList)
                        sys.exit(1)
                    else:
                        self.db.insert(file=fileDir, tag=tag, question=que, answer=ans)
        self.db.create_index('file', 'tag', 'question')
        self.db.commit()
        self.save_data_file_info(self.curFileInfoList)

if __name__ == '__main__':
    insertData()

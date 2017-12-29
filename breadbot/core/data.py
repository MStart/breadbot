#!/usr/bin/env python3
import os
import re
import yaml
from pymongo import MongoClient

from breadbot.core import misc


class Data(object):

    def __init__(self, dataPaths=None):
        self.splitSig = ' '
        if not dataPaths:
            dataPaths = misc.cfg().get('data_path')
        self.dataPaths = dataPaths
        self.db = self._open_db()

    def insert_data(self):
        changedDataList = \
            self._get_changed_data_list(self.dataPaths)
        self._clean_old_db_data(changedDataList)
        self._insert_db_data(changedDataList)
        print('\n All Complete!')

    def drop_db(self):
        client = MongoClient('localhost', 27017)
        client.drop_database(self.db_name)
        print('\n Drop database done.')

    def _open_db(self):
        db_name = misc.cfg().get('db_name')
        ip = misc.cfg().get('db_ip')
        port = misc.cfg().get('db_port')
        client = MongoClient(ip, port)
        return client[db_name]

    def _get_data_log_path(self):
        dataLogPath = os.path.join(misc.cfg().get('log_path'), 'data.log')
        return dataLogPath

    def _get_path_name(self, filePath):
        return re.sub('[^a-zA-Z0-9]', '_', filePath)

    def _read_data_file(self, dataPath):
        f = open(dataPath, 'r')
        readStr = f.read()
        readStr = re.sub(r'\n +\n', '\n\n', readStr)
        f.close()
        return readStr

    def _save_data_list(self, dataList):
        dataLogPath = self._get_data_log_path()
        log = open(dataLogPath, 'w')
        for dataPathInfo in dataList:
            log.write(dataPathInfo + '\n')
        log.close()

    def _get_data_list(self, root, files):
        dataList = []
        for file in files:
            if not re.match(r'^.*\.yml$', file):
                continue
            filePath = os.path.join(root, file)
            editTime = os.stat(filePath).st_mtime
            info = ' '.join([filePath, str(editTime)])
            dataList.append(info)
        return dataList

    def _get_cur_data_list(self, dataPaths):
        curDataList = []
        for dataPath in dataPaths:
            for root, dirs, files in os.walk(dataPath):
                dataList = self._get_data_list(root, files)
                curDataList += dataList
        return curDataList

    def _get_old_data_list(self):
        dataLogPath = self._get_data_log_path()
        if os.path.exists(dataLogPath):
            log = open(dataLogPath, 'r')
            oldDataList = log.readlines()
            for i in range(len(oldDataList)):
                oldDataList[i] = oldDataList[i].replace('\n', '')
            log.close()
            return oldDataList
        else:
            log = open(dataLogPath, 'w')
            log.close()
            return []

    def _get_changed_data_list(self, dataPaths):
        curDataList = self._get_cur_data_list(dataPaths)
        oldDataList = self._get_old_data_list()
        changedDataList = []
        for dataPath in curDataList:
            if dataPath not in oldDataList:
                dataPath = dataPath.split(self.splitSig)[0]
                changedDataList.append(dataPath)
        for dataPath in oldDataList:
            if dataPath not in curDataList:
                dataPath = dataPath.split(self.splitSig)[0]
                changedDataList.append(dataPath)
        self._save_data_list(curDataList)
        return changedDataList

    def _clean_old_db_data(self, changedDataList):
        for dataPath in changedDataList:
            pathName = self._get_path_name(dataPath)
            print('clean %s...' % pathName)
            self.db[pathName].drop()
        for dataPath in changedDataList:
            path = dataPath.split(self.splitSig)[0]
            if not os.path.exists(path):
                changedDataList.remove(dataPath)

    def _insert_db_data(self, changedDataList):
        for dataPath in changedDataList:
            pathName = self._get_path_name(dataPath)
            print('insert %s...' % pathName)
            coll = self.db[pathName]
            readStr = self._read_data_file(dataPath)
            data = yaml.load(readStr)
            coll.insert(data)
            coll.create_index('tag')
            coll.create_index('que')

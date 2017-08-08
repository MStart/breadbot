# They are misc functions
import os
import sys
import urllib.parse
import urllib.request
import time
import re

def baiduSearch(keyword):
    p = {'wd': keyword}
    return "http://www.baidu.com/s?"+urllib.parse.urlencode(p)

def write_log(input_str):
    curDir = os.path.dirname(__file__)
    curDirList = curDir.split('/')
    curDirList.pop()
    upperDir = r'/'.join(curDirList)
    logDir = os.path.join(upperDir, r'data/log')
    curTime = time.strftime('[%Y-%m-%d %H:%M:%S] ',time.localtime())
    text = curTime + input_str
    f = open(logDir,'a')
    f.write(text + '\n')
    f.close()
    return text

def printLog(Str): 
    curTime = time.strftime('[%Y-%m-%d %H:%M:%S] ',time.localtime())
    print(curTime + str(Str))

def get_public_ip():
    reg = 'fk="\d+\.\d+\.\d+\.\d+" '
    url = 'http://www.baidu.com/s?wd=gongwangip'
    result = re.search(reg, str(urllib.request.urlopen(url).read())).group(0)
    result = re.search('\d+\.\d+\.\d+\.\d+',result).group(0)
    return result

def translate(word):
    if re.match(u'.*[\u4e00-\u9fa5].*', word):
        p = {'wd': word}
        return "http://dict.baidu.com/s?"+urllib.parse.urlencode(p)
    result1 = os.popen('sdcv -n ' + word).readlines()
    if not re.match(u'^Found 1 items.*', result1[0]):
        return '[Not Found]'
    res = ''
    for i in range(4,len(result1)):
        res += result1[i]
    res = re.sub(u'\[.+\]','',res) 
    res = res.replace('\n','')
    res = res.replace('//','\r')
    return res

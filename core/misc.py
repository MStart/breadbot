# This are misc functions

import os, sys
import urllib.parse, urllib.request
import time
import re

def baiduSearch(keyword):
    p = {'wd': keyword}
    return "http://www.baidu.com/s?"+urllib.parse.urlencode(p)

def write_log(input_str):
    current_dir = os.path.dirname(__file__)
    current_dir_list = current_dir.split('/')
    current_dir_list.pop()
    upper_dir_list = current_dir_list
    upper_dir = ''
    for path in upper_dir_list:
        upper_dir += path + r'/'
    log_dir = upper_dir + r'data/log.txt'
    this_time = time.strftime('[%Y-%m-%d %H:%M:%S] ',time.localtime())
    text = this_time + input_str
    f = open(log_dir,'a')
    f.write(text + '\n')
    f.close()
    return text

def printLog(Str): 
    this_time = time.strftime('[%Y-%m-%d %H:%M:%S] ',time.localtime())
    print(this_time + str(Str))

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

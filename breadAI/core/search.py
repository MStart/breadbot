import os
import re
import time
import urllib.parse
import urllib.request


def baiduSearch(keyword):
    p = {'wd': keyword}
    return "http://www.baidu.com/s?" + urllib.parse.urlencode(p)


def wikiSearch(keyword):
    keyword = keyword.replace(' ', '_')
    return 'https://en.m.wikipedia.org/wiki/' + keyword


def get_public_ip():
    reg = 'fk="\d+\.\d+\.\d+\.\d+" '
    url = 'http://www.baidu.com/s?wd=gongwangip'
    result = re.search(reg, str(urllib.request.urlopen(url).read())).group(0)
    result = re.search('\d+\.\d+\.\d+\.\d+', result).group(0)
    return result


def translate(word):
    if re.match(u'.*[\u4e00-\u9fa5].*', word) or ' ' in word:
        p = {'wd': word}
        return "http://dict.baidu.com/s?" + urllib.parse.urlencode(p)
    result1 = os.popen('sdcv -n ' + word).readlines()
    if not re.match(u'^Found 1 items.*', result1[0]):
        return '[Not Found]'
    res = ''
    for i in range(4, len(result1)):
        res += result1[i]
    res = re.sub(u'\[.+\]', '', res)
    res = res.replace('\n', '')
    res = res.replace('//', '\r')
    return res

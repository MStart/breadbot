from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.template import loader, Context
from xml.etree import ElementTree as ET
import time
import hashlib
import socket
import os, sys
from breadAI import core

class WeChat(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(WeChat, self).dispatch(*args, **kwargs)
        
    def is_super(self, name):
        super_users = core.misc.get_cfg()['super_users']
        for user in super_users:
            user_name = core.misc.get_cfg()['super_users'][user]
            if user_name == name:
                return True
        return False

    def get(self, request):
        token = 'Mark_Young'
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        list = [token,timestamp,nonce]
        list.sort()
        hashcode = ''.join([s for s in list])
        hashcode = hashlib.sha1(hashcode.encode('ascii')).hexdigest()
        if hashcode == signature:
            return HttpResponse(echostr)

    def post(self, request):
        strXml = ET.fromstring(request.body)
        fromUser = strXml.find('FromUserName').text
        toUser = strXml.find('ToUserName').text
        content = strXml.find('Content').text
        currentTime = str(int(time.time()))
        if self.is_super(fromUser):
            result = core.bot.chat().response(content, True)
        else:
            result = core.bot.chat().response(content, False)
        template = loader.get_template('wechat/text_message_template.xml')
        context = Context({'toUser': fromUser, 'fromUser': toUser, 'currentTime': currentTime, 'content': result})
        contextXml = template.render(context)
        logStr = '\nUser:   ' + fromUser + '\nAsk:    ' + content + '\nAnswer: ' + result + '\n'
        core.misc.write_log(logStr)
        return HttpResponse(contextXml)

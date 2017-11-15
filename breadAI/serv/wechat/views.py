from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.template import loader, Context
import hashlib
import sys
import time
from xml.etree import ElementTree as ET

from breadAI import core


class WeChat(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(WeChat, self).dispatch(*args, **kwargs)

    def is_super(self, name):
        super_users = core.misc.cfg().get('super_users')
        for user in super_users:
            if user == name:
                return True
        return False

    def get(self, request):
        token = 'Mark_Young'
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        list = [token, timestamp, nonce]
        list.sort()
        hashcode = ''.join([s for s in list])
        hashcode = hashlib.sha1(hashcode.encode('ascii')).hexdigest()
        if hashcode == signature:
            return HttpResponse(echostr)

    def post(self, request):
        strXml = ET.fromstring(request.body)
        fromUser = strXml.find('FromUserName').text
        toUser = strXml.find('ToUserName').text
        currentTime = str(int(time.time()))
        msgType = strXml.find('MsgType')
        if msgType:
            msgType = msgType.text
        content = strXml.find('Content')
        if content:
            content = content.text
        if msgType == 'text':
            if self.is_super(fromUser):
                result = core.chat().response(content, True)
            else:
                result = core.chat().response(content, False)
        else:
            result = 'Sorry, I only support text chatting'
        template = loader.get_template('wechat/text_message_template.xml')
        context = Context({'toUser': fromUser,
                           'fromUser': toUser,
                           'currentTime': currentTime,
                           'content': result})
        contextXml = template.render(context)
        logStr = '\nUser:   %s\nAsk:    %s\nAnswer: %s\n' % \
                 (fromUser, content, result)
        core.misc.log().write(logStr)
        return HttpResponse(contextXml)

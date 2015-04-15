from django.shortcuts import render
from django.http import HttpResponse
import hashlib
import lxml
import time
import os
from lxml import etree

####### TEST ###############
import datetime
#from django.template.loader import get_template
#from django.template import Context
from django.shortcuts import render_to_response
import traceback

####### END of TEST ########

# Create your views here.
def home(req):
    print '---> in home'
    print 'host: ', req.get_host()
    print 'path: ', req.get_full_path()
    print 'body: ', req.body
    print 'method: ', req.method
    print '---> after print'

    if req.method == 'GET' and 'signature' in req.GET:
        signature = req.GET['signature']
        echostr = req.GET['echostr']
        timestamp = req.GET['timestamp']
        nonce = req.GET['nonce']

        token = '1stloop'
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            return HttpResponse(echostr) 
        return HttpResponse('end of get') 
    if req.method == 'POST':
        print '---> in POST'
        str_xml = req.body
        xml = etree.fromstring(str_xml)
        content = xml.find("Content").text
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        print content, msgType, fromUser, toUser
        return render_to_response('wx_reply_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': content})
        


def test(req):
    print '---> in test'
    print req.body
    now = datetime.datetime.now()
    #assert False
    return render_to_response('now.template.html', {'current_date': now})

###
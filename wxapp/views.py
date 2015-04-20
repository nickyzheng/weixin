# -*- coding: utf-8 -*-

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
import logging
import urlparse
import urllib
import random
import string
import re

from wxapp.models import clothes

####### END of TEST ########

# Create your views here.
logger = logging.getLogger(__name__)

def home(req):
    request_message = '\n'
    request_message += get_client_ip(req) + ', '
    request_message += req.method + ', '
    request_message += req.get_full_path() + ', '
    logger.info(request_message)
    logger.info(req.body)

    if req.method == 'GET' and 'signature' in req.GET:
        signature = req.GET['signature']
        echostr = req.GET['echostr']
        timestamp = req.GET['timestamp']
        nonce = req.GET['nonce']

        if check_signature(timestamp, nonce, signature):
            return HttpResponse(echostr) 
        return HttpResponse('end of get') 
    if req.method == 'POST':
        url = req.get_full_path()
        parsed = urlparse.urlparse(url)
        signature = urlparse.parse_qs(parsed.query)['signature'][0]
        timestamp = urlparse.parse_qs(parsed.query)['timestamp'][0]
        nonce = urlparse.parse_qs(parsed.query)['nonce'][0]
        if not check_signature(timestamp, nonce, signature):
            return HttpResponse('Check signature failed.') 
        str_xml = req.body
        xml = etree.fromstring(str_xml)
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        msgType = xml.find("MsgType").text
        if msgType == 'text':
            content = xml.find("Content").text.lower()
            pattern_show = r'^show'
            p = re.compile(pattern_show)
            if p.match(content):
                command = content.split()
                if command[0] == 'show':
                    c = clothes.objects.get(name = command[1])
                    reply_content = u'查询结果：\n'
                    reply_content += 'name: ' + c.name + '\n'
                    reply_content += 'category: ' + c.category + '\n'
                    reply_content += 'season: ' + c.season + '\n'
                    reply_content += 'tag: ' + c.tag + '\n'
                    reply_content += u'选择次数: ' + str(c.choose_count)
                    image_url_prefix = 'http://1stloop.com/'
                    picUrl = image_url_prefix + c.image_filename
                    return render_to_response('wx_reply_image_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content, 'picUrl': picUrl})
                if command[0] == 'showall':
                    all_clothes = clothes.objects.all()
                    reply_content = u'所有的衣服：\n'
                    for c in all_clothes:
                        reply_content += c.name + '\n'
                if command[0] == 'showpic':
                    reply_content = str(datetime.datetime.now()) + ' ' + content
            else:       
                reply_content = 'No match!'
        if msgType == 'image':
            PicUrl = xml.find("PicUrl").text
            new_filename = ''.join(random.choice(string.lowercase) for x in range(5)) + '.jpg'
            new_filename = 'static/upload/' + new_filename
            urllib.urlretrieve(PicUrl, new_filename)
            new_name = '新衣服' + str(clothes.objects.all().order_by('-id')[0].id + 1)
            new_clothes = clothes.objects.create(name = new_name, image_filename = new_filename)
            reply_content = new_name + ' 已保存'
        return render_to_response('wx_reply_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content})
        
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def check_signature(timestamp, nonce, signature):
    token = '1stloop'
    list = [token, timestamp, nonce]
    list.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, list)
    hashcode = sha1.hexdigest()
    if hashcode == signature:
        logger.info('Check signature success.')
        return True
    else:
        logger.info('Check signature fail.')
        return False


def test(req):
    print '---> in test'
    print req.body
    now = datetime.datetime.now()
    #assert False
    
    logger.info('aaa')
    logger.error('bbb')

    new_name = '新衣服'

    new_name += str(clothes.objects.all().order_by('-id')[0].id + 1)

    new_filename = ''.join(random.choice(string.lowercase) for x in range(5)) + '.jpg'

    new_clothes = clothes.objects.create(name = new_name, image_filename = new_filename)

    return render_to_response('now.template.html', {'current_date': now})

###
###
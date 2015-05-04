# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import hashlib
import lxml
import time
import os
from lxml import etree
import qimila

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
from wxapp.models import user

####### END of TEST ########

# Create your views here.
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
        image_text_reply_content = u'查询结果：\n'
        image_text_reply_content += 'name: %s \n'
        image_text_reply_content += 'category: %s \n'
        image_text_reply_content += 'season: %s \n'
        image_text_reply_content += 'tag: %s \n'
        image_text_reply_content += u'选择次数: %s'
        image_url_prefix = 'http://1stloop.com/static/upload/'

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
                    c = clothes.objects.filter(name__startswith = command[1], user__openid = fromUser)[0]
                    reply_content = set_image_text_reply_content(c)
                    picUrl = image_url_prefix + c.image_filename
                    Url = 'http://1stloop.com/detail/%s' % (c.id)
                    return render_to_response('wx_reply_image_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content, 'picUrl': picUrl, 'Url': Url})
                if command[0] == 'showall':
                    all_clothes = clothes.objects.filter(user__openid = fromUser)
                    reply_content = u'共有 ' + str(all_clothes.count()) + u' 件衣服：\n'
                    for c in all_clothes:
                        reply_content += c.name + '\n'
                    return render_to_response('wx_reply_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content})
                if command[0] == 'showcat':
                    all_clothes = clothes.objects.filter(category = command[1], user__openid = fromUser)
                    reply_content = u'本类型衣服共有 ' + str(all_clothes.count()) + u' 件\n'
                    for c in all_clothes:
                        reply_content += c.name + '\n'
                    return render_to_response('wx_reply_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content})
                if command[0] == 'showsea':
                    all_clothes = clothes.objects.filter(season = command[1], user__openid = fromUser)
                    reply_content = u'本季衣服共有 ' + str(all_clothes.count()) + u' 件\n'
                    for c in all_clothes:
                        reply_content += c.name + '\n'
                    return render_to_response('wx_reply_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content})

            pattern_rename = r'^rename'
            p = re.compile(pattern_rename)
            if p.match(content):
                command = content.split()
                c = clothes.objects.get(name = command[1], user__openid = fromUser)
                c.name = command[2]
                c.save()
                reply_content = set_image_text_reply_content(c)
                picUrl = image_url_prefix + c.image_filename
                return render_to_response('wx_reply_image_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content, 'picUrl': picUrl})

            pattern_set = r'^set'
            p = re.compile(pattern_set)
            if p.match(content):
                command = content.split()
                if command[1] == 'category' or command[1] == 'cat':
                    c = clothes.objects.get(name = command[2], user__openid = fromUser)
                    c.category = command[3]
                    c.save()
                if command[1] == 'season' or command[1] == 'sea':
                    c = clothes.objects.get(name = command[2], user__openid = fromUser)
                    c.season = command[3]
                    c.save()

                reply_content = set_image_text_reply_content(c)
                picUrl = image_url_prefix + c.image_filename
                return render_to_response('wx_reply_image_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content, 'picUrl': picUrl})

            pattern_today = r'^today'
            p = re.compile(pattern_today)
            if p.match(content):
                command = content.split()
                c = clothes.objects.filter(category = command[1], season = command[2], user__openid = fromUser).order_by('?')[0]
                reply_content = set_image_text_reply_content(c)
                picUrl = image_url_prefix + c.image_filename
                return render_to_response('wx_reply_image_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content, 'picUrl': picUrl})

            pattern_del = r'^del'
            p = re.compile(pattern_del)
            if p.match(content):
                command = content.split()
                c = clothes.objects.get(name = command[1], user__openid = fromUser)
                name = c.name
                filename = c.image_filename
                c.delete()
                os.remove(BASE_DIR + '/static/upload/' + filename)
                reply_content = name + u' 已删除'
                return render_to_response('wx_reply_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content})

            pattern_choose = r'^choose'
            p = re.compile(pattern_choose)
            if p.match(content):
                command = content.split()
                c = clothes.objects.get(name = command[1], user__openid = fromUser)
                c.choose_count += 1
                c.save()
                reply_content = set_image_text_reply_content(c)
                picUrl = image_url_prefix + c.image_filename
                return render_to_response('wx_reply_image_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content, 'picUrl': picUrl})

            p = re.compile(r'q')
            if p.match(content):
                reply_content = qimila.get_show()
                return render_to_response('wx_reply_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content})

            # nothing match, display menu        
            reply_content = u'帮助菜单\nrename 给衣服起个名字\nset cat 设置类型\n  1 - business\n  2 - business casual\n  3 - casual\n  4 - sport\nset sea 设置季节\n  1 - spring and autumn\n  2 - summer\n  3 - winter\nshowcat 按类型查找\nshowsea 按季节查找\nshow 显示衣服\nshowall 列出全部衣服\ntoday cat sea 今天穿什么\ndel 删除\nchoose 今天选这件'
            return render_to_response('wx_reply_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content})

           

        if msgType == 'image':
            PicUrl = xml.find("PicUrl").text
            new_filename = ''.join(random.choice(string.lowercase) for x in range(5)) + '.jpg'
            new_filename = new_filename
            urllib.urlretrieve(PicUrl, BASE_DIR + '/static/upload/' + new_filename)
            max_num = '1'
            if clothes.objects.all():
                max_num = str(clothes.objects.all().order_by('-id')[0].id + 1)
            new_name = '新衣服' + max_num
            this_user = user.objects.get(openid = fromUser)
            new_clothes = clothes.objects.create(name = new_name, image_filename = new_filename, user_id = this_user.id)
            reply_content = new_name + '已保存'
            picUrl = image_url_prefix + new_clothes.image_filename
            Url = 'http://1stloop.com/detail/%s' % (new_clothes.id)
            return render_to_response('wx_reply_image_text.xml', {'fromUser': toUser, 'toUser': fromUser, 'createTime': int(time.time()), 'content': reply_content, 'picUrl': picUrl, 'Url': Url})
            
        
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

def set_image_text_reply_content(c):
    image_text_reply_content = u'查询结果：\n'
    image_text_reply_content += 'name: %s \n'
    image_text_reply_content += 'category: %s \n'
    image_text_reply_content += 'season: %s \n'
    image_text_reply_content += 'tag: %s \n'
    image_text_reply_content += u'选择次数: %s'
    if c.category and not c.category.isspace():   
        category = clothes.CATEGORY_LIST[int(c.category) - 1][1]
    else:
        category = 'not set'
    if c.season and not c.season.isspace():
        season = clothes.SEASON_LIST[int(c.season) - 1][1]
    else:
        season = 'not set'
    reply_content = image_text_reply_content % (c.name, category, season, c.tag, str(c.choose_count))
    return reply_content

def clothes_detail(req, clothes_id):
    if req.method == 'GET':
        print '---> clothes_id:', clothes_id
        c = clothes.objects.get(id = clothes_id)
        return render_to_response('clothes_detail.html', {'clothes': c})
    if req.method == 'POST':
        category = req.POST.get('category')
        season = req.POST.get('season')
        name = req.POST.get('name')
        c = clothes.objects.get(id = clothes_id)
        c.name = name
        c.category = category
        c.season = season
        c.save()
        return HttpResponseRedirect('/detail/%s' % (c.id))

def test(req):
    print '---> in test'
    print req.body
    now = datetime.datetime.now()
    #assert False
    
    logger.info('aaa')
    logger.error('bbb')

    return HttpResponse('success')

    #return render_to_response('starter-template.html', {'image_url': 'http://1stloop.com/static/upload/frroo.jpg'})

###
###
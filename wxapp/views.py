from django.shortcuts import render
from django.http import HttpResponse
import hashlib

# Create your views here.
def home(req):
    print '------> ', req
    if 'signature' in req.GET:
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

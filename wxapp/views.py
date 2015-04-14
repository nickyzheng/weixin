from django.shortcuts import render
from django.http import HttpResponse
import hashlib

####### TEST ###############
import datetime
#from django.template.loader import get_template
#from django.template import Context
from django.shortcuts import render_to_response

####### END of TEST ########

# Create your views here.
def home(req):
    print req
    if req.method == 'GET':
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
    if req.method == 'POST':
        print req
        return

def test(req):
    now = datetime.datetime.now()
    #assert False
    return render_to_response('now.template.html', {'current_date': now})
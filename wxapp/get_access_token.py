
#https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET

#wx879e0093e804cd74
#acbb354adc7dcae4380e5c3d42d04b5e

import requests

appid = 'wx879e0093e804cd74'
secret = 'acbb354adc7dcae4380e5c3d42d04b5e'

host = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, secret)

session = requests.Session()

resp = session.get(host)

resp_json = resp.json()

print resp_json
print resp_json['access_token']

f = open('access_token.txt', 'w+')
f.write(resp_json['access_token'])
f.close
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import requests
import os

def get_show():
	qimila_latest_url = 'http://qimila.net/portal.php?mod=list&catid=1'
	main_url = 'http://qimila.net/'

	r = requests.get(qimila_latest_url)

	if r.status_code != 200:
		print '[-]', 'status_code =', r.status_code
		os.exit()

	soup = BeautifulSoup(r.text)

	# for item in soup.find_all('a', title=re.compile(u'少康战情')):
	# 	print item['title']
	# 	print item['href']

	item1 = soup.find_all('a', title=re.compile(u'少康战情'))[0]
	item2 = soup.find_all('a', title=re.compile(u'丽文'))[0]

	if item1:
		item1_url = main_url + item1['href']
		print '[+]', item1_url
		r = requests.get(item1_url)
		soup = BeautifulSoup(r.text)
		item1_baidu = soup.find_all('a', href=re.compile(r'pan\.baidu'))[0]['href']
		print '[+]', 'item1_baidu', item1_baidu

	if item2:
		item2_url = main_url + item2['href']
		print '[+]', item2_url
		r = requests.get(item2_url)
		soup = BeautifulSoup(r.text)
		item2_baidu = soup.find_all('a', href=re.compile(r'pan\.baidu'))[0]['href']
		print '[+]', 'item2_baidu', item2_baidu

	msg = item1['title'] + '\n'
	msg += item1_baidu + '\n'
	msg += item2['title'] + '\n'
	msg += item2_baidu

	return msg

if __name__ == "__main__":
	get_show()
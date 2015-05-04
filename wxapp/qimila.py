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

	keywords = []

	# keywords.append(u'文茜')
	keywords.append(u'少康战情')
	# keywords.append(u'丽文')


	return get_baidu_link(soup, keywords)

def get_baidu_link(soup, keywords):
	main_url = 'http://qimila.net/'
	msg = ''

	for keyword in keywords:
		item = soup.find_all('a', title = re.compile(keyword))[0]
		if item:
			item_url = main_url + item['href']
			print '[+]', item_url
			r = requests.get(item_url)
			item_soup = BeautifulSoup(r.text)
			item_baidu = item_soup.find_all('a', href=re.compile(r'pan\.baidu'))[0]['href']
			print '[+]', item_baidu
			msg += item['title'] + '\n'
			msg += item_baidu + '\n'

	return msg

if __name__ == "__main__":
	get_show()
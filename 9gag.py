#!/usr/bin/env python
import pyperclip,os,time,urllib.request,sys
from bs4 import BeautifulSoup
from urllib.request import urlopen
from os.path import expanduser, splitext
from multiprocessing import Process
from urllib.parse import urlparse

desktop = expanduser("~") + '/Desktop'
new = pyperclip.paste()
parsed_url = urlparse(new)

if len(sys.argv) < 2:
	if bool(parsed_url.scheme):
		print('Clipboard URL is valid.')
	else:
		print('9GAG post url need to be provided as parameter.')
		exit(0)
elif len(sys.argv) < 3:
	new = sys.argv[1]
else:
	print('Post url need to be provided as parameter or copied to clipboard.')

def download_file(url, filename):
	urllib.request.urlretrieve(url, desktop + '/' + filename)
	return

def get_ext(url):
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ext

def gag(url):
	print('9gag')
	page = urlopen(url)
	soup = BeautifulSoup(page, 'lxml')
	title = soup.find('meta',  property = 'og:title')
	title = title['content']
	print(title)

	# video
	video = soup.find('source', type = 'video/mp4')

	if video is not None:
		url = video['src']
	else:
		image = soup.find('meta', property = 'og:image')
		url = image['content']

	filename = title + get_ext(url)
	print(url)
	
	download_file(url, filename)
	return

if __name__ == '__main__':
	#new = pyperclip.paste()
	gag(new)
	#print(get_ext('https://images-cdn.9gag.com/photo/abpDe2L_700b.jpg'))
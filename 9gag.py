#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name      : 9GAG Media Downloader
# Purpose   : Python script which downloads the 9GAG media from the provided 9gag.com post url in highest quality.
#
# Author   : SirDavalos
# Created   : 8 Nov 2017
# Copyright : (c) https://github.com/sirdavalos
# Licence   : MIT
#-------------------------------------------------------------------------------
import pyperclip,os,time,urllib.request,sys,progressbar
from bs4 import BeautifulSoup
from urllib.request import urlopen
from os.path import expanduser, splitext
from urllib.parse import urlparse

desktop = expanduser("~") + '/Desktop'
new = pyperclip.paste()
parsed_url = urlparse(new)
pbar = None

def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

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
	urllib.request.urlretrieve(url, desktop + '/' + filename, show_progress)
	return

def get_ext(url):
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ext

def gag(url):
	print('9gag')
	print("url: " + url)
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

	# Clear from filename
	chars = ['📌','/','\\',':',';','?','*','<','>','|','\"']
	for x in chars:
		if x in title:
			title = title.replace(x, "")
	title = title.rstrip()
	title = title.lstrip()
	filename = title + get_ext(url)
	print(url)
	
	download_file(url, filename)
	return

if __name__ == '__main__':
	#new = pyperclip.paste()
	gag(new)
	#print(get_ext('https://images-cdn.9gag.com/photo/abpDe2L_700b.jpg'))
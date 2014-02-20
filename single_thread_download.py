#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# single_thread_download.py


import os
import urllib.request
import urllib.error
import shutil


def single_thread_download(url, file_name=None, overwrite=False):
	# 如果文件名为空，则从 URL 中获取文件名
	if file_name is None:
		file_name = url.rpartition('/')[-1]
	# 潜在 bug：如果不覆盖己有文件，而已有文件不完整（eg. 没下载全），会有潜在影响
	if os.path.exists(file_name) and (not overwrite):
		return
	try:
		with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_stream:
			shutil.copyfileobj(response, out_stream)
	except urllib.error.URLError as e:
		print(e.errno, '\n', e.reason, '\n')

# single_thread_download("http://screencasts.b0.upaiyun.com/podcasts/nil_podcast_1.m4a")



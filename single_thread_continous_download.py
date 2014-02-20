#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# single_thread_continous_download.py


import os
import urllib.request
import urllib.error
import shutil

import utility
from utility import get_file_size


def single_thread_continous_download(url, file_name=None, overwrite=False):
	# 如果文件名为空，则从 URL 中获取文件名
	if file_name is None:
		file_name = url.rpartition('/')[-1]
	begin = 0			# 断点续传起始下载偏移量，默认为 0，从头开始
	if os.path.exists(file_name) and (not overwrite):
		target_size = get_file_size(url)
		if (target_size < 0):
			print("single_thread_continous_download(): get_file_size() error!")
			return
		current_size = os.path.getsize(file_name)
		if (current_size < target_size):
			begin = current_size
		elif (current_size == target_size):
			print("single_thread_continous_download(): file download complete!")
			return 
		else:
			print("single_thread_continous_download(): file size exception, current file size bigger than target file size!")
			return 
	req = urllib.request.Request(url)
	req.add_header('Range', 'bytes=%d-' % (begin))
	try:
		with urllib.request.urlopen(req) as response, open(file_name, 'ab+') as out_stream:
			shutil.copyfileobj(response, out_stream)
	except urllib.error.URLError as e:
		print(e.errno, '\n', e.reason, '\n')

# single_thread_continous_download("http://screencasts.b0.upaiyun.com/podcasts/nil_podcast_1.m4a")



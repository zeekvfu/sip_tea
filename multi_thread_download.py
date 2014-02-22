#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# multi_thread_download.py


import os
import threading
import urllib.request
import urllib.error
import shutil

import utility
from utility import get_file_size
from utility import split_file_size
from utility import split_file_name
from utility import append_file

import single_thread_download
from single_thread_download import single_thread_download


# 各个子线程下载自己负责的那部分内容
def sub_thread_download(url, file_name, begin, end):
	req = urllib.request.Request(url)
	req.add_header('Range', 'bytes=%d-%d' % (begin, end))
	try:
		with urllib.request.urlopen(req) as response, open(file_name, 'wb') as out_stream:
			shutil.copyfileobj(response, out_stream)
	except urllib.error.URLError as e:
		print(e.errno, '\n', e.reason, '\n')


# 多线程
def multi_thread_download(url, file_name=None, overwrite=False, thread_num=4):
	if thread_num == 1:
		single_thread_download(url, file_name, overwrite)
	elif thread_num > 1:
		# 如果文件名为空，则从 URL 中获取文件名
		if file_name is None:
			file_name = url.rpartition('/')[-1]
		# 潜在 bug：如果不覆盖己有文件，而已有文件不完整（eg. 没下载全），会有潜在影响
		if os.path.exists(file_name) and (not overwrite):
			return
		target_size = get_file_size(url)
		if (target_size < 0):
			print("multi_thread_download(): get_file_size() error!\n")
			return
		ranges = split_file_size(target_size, thread_num)
		thread_group = []
		for i in range(thread_num):
			# print(i, '\t', ranges[i][0], ',', ranges[i][1])
			t = threading.Thread(target=sub_thread_download, name="thread%d" % i, args=(url, split_file_name(file_name, i), ranges[i][0], ranges[i][1]))
			t.start()
			thread_group.append(t)
		for t in thread_group:
			t.join()
		append_file(file_name, thread_num, False)


multi_thread_download("http://screencasts.b0.upaiyun.com/podcasts/nil_podcast_1.m4a", overwrite=False, thread_num=4)
# multi_thread_download("http://iweb.dl.sourceforge.net/project/zsh/zsh-doc/5.0.5/zsh-5.0.5-doc.tar.bz2", overwrite=True, thread_num=4)
# multi_thread_download("https://github.com/zeekvfu/sip_tea/archive/master.zip", overwrite=True, thread_num=4)





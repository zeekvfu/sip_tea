#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# multi_thread_continous_download.py


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

import single_thread_continous_download
from single_thread_continous_download import single_thread_continous_download


# 各个子线程下载自己负责的那部分内容
def sub_thread_continous_download(url, file_name, begin, end):
	_begin = begin
	if os.path.exists(file_name):
		target_size = end - begin + 1
		if (target_size < 0):
			print("sub_thread_continous_download(): file size error!")
			return
		current_size = os.path.getsize(file_name)
		# 此处认为已存在的同名文件，就是要下载的目标文件，只是未下载完而已，可以继续下载
		if (current_size < target_size):
			_begin += current_size
		elif (current_size == target_size):
			print("sub_thread_continous_download(): file download complete!")
			return 
		# 已存在的同名文件大小 > 要下载的目标文件大小，重命名已存在文件，重新下载目标文件
		else:
			print("sub_thread_continous_download(): file size exception, current file size bigger than target file size!")
			new_file_name = file_name + '.backUP'
			os.rename(file_name, new_file_name)
			print("sub_thread_continous_download(): %s renamed to %s ..." % (file_name, new_file_name))
	req = urllib.request.Request(url)
	req.add_header('Range', 'bytes=%d-%d' % (_begin, end))
	try:
		with urllib.request.urlopen(req) as response, open(file_name, 'ab+') as out_stream:
			shutil.copyfileobj(response, out_stream)
	except urllib.error.URLError as e:
		print(e.errno, '\n', e.reason, '\n')


# 多线程，断点续传
def multi_thread_continous_download(url, file_name=None, overwrite=False, thread_num=4):
	if thread_num == 1:
		single_thread_continous_download(url, file_name, overwrite)
	elif thread_num > 1:
		# 如果文件名为空，则从 URL 中获取文件名
		if file_name is None:
			file_name = url.rpartition('/')[-1]
		target_size = get_file_size(url)
		if (target_size < 0):
			print("multi_thread_continous_download(): get_file_size() error!\n")
			return
		if os.path.exists(file_name) and (not overwrite):
			current_size = os.path.getsize(file_name)
			if (current_size == target_size):
				print("multi_thread_continous_download(): file download complete!")
				return 
			# 已存在的同名文件大小 != 要下载的目标文件大小，重命名已存在文件，重新下载目标文件
			else:
				print("multi_thread_continous_download(): file size exception, current file size and target file size NOT same!")
				new_file_name = file_name + '.backUP'
				os.rename(file_name, new_file_name)
				print("multi_thread_continous_download(): %s renamed to %s ..." % (file_name, new_file_name))
		ranges = split_file_size(target_size, thread_num)
		thread_group = []
		for i in range(thread_num):
			# print(i, '\t', ranges[i][0], ',', ranges[i][1])
			t = threading.Thread(target=sub_thread_continous_download, name="thread%d" % i, args=(url, split_file_name(file_name, i), ranges[i][0], ranges[i][1]))
			t.start()
			thread_group.append(t)
		for t in thread_group:
			t.join()
		append_file(file_name, thread_num, True)


multi_thread_continous_download("http://screencasts.b0.upaiyun.com/podcasts/nil_podcast_1.m4a", overwrite=False, thread_num=4)
# multi_thread_continous_download("http://iweb.dl.sourceforge.net/project/zsh/zsh-doc/5.0.5/zsh-5.0.5-doc.tar.bz2", overwrite=True, thread_num=4)
# multi_thread_continous_download("https://github.com/zeekvfu/sip_tea/archive/master.zip", overwrite=True, thread_num=4)





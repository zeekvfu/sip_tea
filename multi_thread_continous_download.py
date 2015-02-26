#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# multi_thread_continous_download.py


import os, threading
import urllib.request, urllib.error
import shutil

import socket
# from socket import timeout

import utility
from utility import get_current_timestamp, get_file_size, split_file_size, get_file_name_split, check_file_integrity, append_file

import single_thread_continous_download
from single_thread_continous_download import single_thread_continous_download




# 各个子线程下载自己负责的那部分内容
def sub_thread_continous_download(url, file_name, begin, end, target_size, timeout_retry=True):
	while True:
		_begin = begin
		if os.path.exists(file_name):
			if (target_size < 0):
				print("sub_thread_continous_download(): file target_size < 0!")
				return
			current_size = os.path.getsize(file_name)
			# 此处认为已存在的同名文件，就是要下载的目标文件；只是未下载完而已，可以继续下载
			if (current_size < target_size):
				_begin += current_size
			# 理论上来说，更严谨的方法是下载完目标文件，然后比较两个文件的 MD5 值。但是需要事先下载整个文件，浪费带宽（尤其是文件很大的时侯）
			elif (current_size == target_size):
				print("sub_thread_continous_download(): file %s already downloaded complete!" %(file_name))
				return 
			# 已存在的同名文件大小 > 要下载的目标文件大小，重命名已存在文件，重新下载目标文件
			else:
				print("sub_thread_continous_download(): file size exception, current_size > target_size!")
				new_file_name = file_name + '_' + get_current_timestamp()
				os.rename(file_name, new_file_name)
				print("sub_thread_continous_download(): %s RENAMED TO %s" %(file_name, new_file_name))
		req = urllib.request.Request(url)
		req.add_header('Range', 'bytes=%d-%d' % (_begin, end))
		try:
			with urllib.request.urlopen(req, timeout=300) as response, open(file_name, 'ab+') as out_stream:
				shutil.copyfileobj(response, out_stream)
			return 
		except urllib.error.URLError as e:
			print("sub_thread_continous_download(): urllib.error.URLError\t", url, "\t", e.errno, "\t", e.reason)
			return 
		except socket.timeout:
			print('sub_thread_continous_download(): socket.timeout')
			if not timeout_retry:
				break
		except ConnectionResetError:
			print("sub_thread_continous_download(): ConnectionResetError")
			return
	return 


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
		if os.path.exists(file_name):
			if overwrite:
				os.remove(file_name)
			current_size = os.path.getsize(file_name)
			# 理论上来说，更严谨的方法是下载完目标文件，然后比较两个文件的 MD5 值。但是需要事先下载整个文件，可能浪费带宽（尤其是文件很大的时侯）
			if (current_size == target_size):
				print("multi_thread_continous_download(): file %s already downloaded complete!" %(file_name))
				return 
			# 已存在的同名文件大小 != 要下载的目标文件大小，重命名已存在文件，重新下载目标文件
			else:
				print("multi_thread_continous_download(): file %s size exception, current_size != target_size" %(file_name))
				new_file_name = file_name + '_' + get_current_timestamp()
				os.rename(file_name, new_file_name)
				print("multi_thread_continous_download(): %s RENAMED TO %s" %(file_name, new_file_name))
		ranges = split_file_size(target_size, thread_num)
		thread_group = []
		for i in range(thread_num):
			# print(i, '\t', ranges[i][0], ',', ranges[i][1])
			t = threading.Thread(target=sub_thread_continous_download, name="thread%d" % i, args=(url, get_file_name_split(file_name, i), ranges[i][0], ranges[i][1], ranges[i][2]))
			t.start()
			thread_group.append(t)
		for t in thread_group:
			t.join()
		# 拼接前检查各个文件块的完整性
		if check_file_integrity(file_name, target_size, thread_num):
			append_file(file_name, thread_num)

# multi_thread_continous_download("http://iweb.dl.sourceforge.net/project/zsh/zsh-doc/5.0.5/zsh-5.0.5-doc.tar.bz2", overwrite=True, thread_num=4)
# multi_thread_continous_download("https://github.com/zeekvfu/sip_tea/archive/master.zip", overwrite=True, thread_num=4)
# multi_thread_continous_download("http://screencasts.b0.upaiyun.com/podcasts/nil_podcast_1.m4a", overwrite=False, thread_num=4)


# url = str(input('请输入要下载的目标文件的 URL：'))
# multi_thread_continous_download(url, thread_num=4)





#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# single_thread_continous_download.py


import os
import urllib.request, urllib.error
import shutil

import utility
from utility import get_current_timestamp, get_file_size




# 单线程，断点续传
def single_thread_continous_download(url, file_name=None, overwrite=False):
	# 如果文件名为空，则从 URL 中获取文件名
	if file_name is None:
		file_name = url.rpartition('/')[-1]
	target_size = get_file_size(url)
	if (target_size < 0):
		print("single_thread_continous_download(): get_file_size() error!")
		return
	begin = 0			# 断点续传起始下载偏移量，默认为 0，从头开始
	if os.path.exists(file_name):
		if overwrite:
			os.remove(file_name)
		current_size = os.path.getsize(file_name)
		# 此处认为已存在的同名文件，就是要下载的目标文件；只是未下载完而已，可以继续下载
		if (current_size < target_size):
			begin = current_size
		# 理论上来说，更严谨的方法是下载完目标文件，然后比较两个文件的 MD5 值。但是需要事先下载整个文件，可能浪费带宽（尤其是文件很大的时侯）
		elif (current_size == target_size):
			print("single_thread_continous_download(): file %s already downloaded complete!" %(file_name))
			return 
		# 已存在的同名文件大小 > 要下载的目标文件大小，重命名已存在文件，重新下载目标文件
		else:
			print("single_thread_continous_download(): file %s size exception, current_size != target_size" %(file_name))
			new_file_name = file_name + '_' + get_current_timestamp()
			os.rename(file_name, new_file_name)
			print("single_thread_continous_download(): %s RENAMED TO %s" %(file_name, new_file_name))
	req = urllib.request.Request(url)
	req.add_header('Range', 'bytes=%d-' % (begin))
	try:
		with urllib.request.urlopen(req) as response, open(file_name, 'ab+') as out_stream:
			shutil.copyfileobj(response, out_stream)
	except urllib.error.URLError as e:
		print("single_thread_continous_download(): urllib.error.URLError\t", url, "\t", e.errno, "\t", e.reason)
	except socket.timeout:
		print('single_thread_continous_download(): socket.timeout ...')
	except ConnectionResetError:
		print("single_thread_continous_download(): ConnectionResetError")

# single_thread_continous_download("http://screencasts.b0.upaiyun.com/podcasts/teahour_episode_70.m4a")


# url = str(input('请输入要下载的目标文件的 URL：'))
# single_thread_continous_download(url)





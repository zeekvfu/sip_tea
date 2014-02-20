#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# utility.py


import urllib.request
import urllib.error

import math


# 得到文件的大小
def get_file_size(url):
	try:
		with urllib.request.urlopen(url) as response:
			headers = response.info()
		if 'Content-Length' in headers:
			return int(headers['Content-Length'])
		else:
			return -1
	except urllib.error.URLError as e:
		print(e.errno, '\n', e.reason, '\n')


# 对文件大小进行切割，以供各个线程分别下载
def split_file_size(file_size, block_count=4):
	ranges = []
	block_size = math.floor(file_size/block_count)
	for i in range(block_count-1):
		# 文件内容字节范围 [begin, end]，左右都是闭区间
		ranges.append((i*block_size, (i+1)*block_size-1))
	ranges.append(((block_count-1)*block_size, file_size-1))
	# print(ranges)
	return ranges



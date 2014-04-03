#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# utility.py


import os
import urllib.request
import urllib.error
import math


# 得到文件的大小
def get_file_size(url):
	try:
		with urllib.request.urlopen(url) as response:
			headers = response.info()
			# print(headers)
			if 'Content-Length' in headers:
				return int(headers['Content-Length'])
			else:
				return -1
	except urllib.error.URLError as e:
		print(e.errno, '\n', e.reason, '\n')
		return -1


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


# 对文件进行切割后，各个文件块的文件名
def split_file_name(file_name, block_no):
	return (file_name + '_part'+ str(block_no))


# 对各个文件块进行拼接，形成最终的文件
def append_file(file_name, block_count, remove_file_block=True):
	with open(file_name, 'wb') as out_stream:
		for i in range(block_count):
			tmp_file_name = split_file_name(file_name, i)
			with open(tmp_file_name, 'rb') as tmp_out_stream:
				out_stream.write(tmp_out_stream.read())
			if remove_file_block:
				os.remove(tmp_file_name)



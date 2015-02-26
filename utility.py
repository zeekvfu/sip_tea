#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# utility.py


import os, datetime, math
import urllib.request, urllib.error

import socket
# from socket import timeout




# get current timestamp
def get_current_timestamp():
	return datetime.datetime.now().strftime('%Y.%m.%d-%H.%M.%S')


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
		print("get_file_size(): urllib.error.URLError\t", url, "\t", e.errno, "\t", e.reason)
		return -1
	except socket.timeout:
		print('get_file_size(): socket.timeout')
		return -1
	except ConnectionResetError:
		print("get_file_size(): ConnectionResetError")
		return -1


# 对文件大小进行切割，以供各个线程分别下载（计数从 0 开始）
def split_file_size(file_size, block_count=4):
	ranges = []
	block_size = math.floor(file_size/block_count)
	for i in range(block_count-1):
		# 文件内容字节范围 [begin, end]，左右都是闭区间
		ranges.append((i*block_size, (i+1)*block_size-1, block_size))
	ranges.append(((block_count-1)*block_size, file_size-1, file_size-(block_count-1)*block_size))
	# print(ranges)
	return ranges


# 对文件进行切割后，各个文件块的文件名
def get_file_name_split(file_name, block_no):
	return (file_name + '_part'+ str(block_no))


# 检查文件（各个块）的完整性（是否存在、是否完整）
def check_file_integrity(file_name, target_size, block_count=4):
	if block_count == 1:
		if not os.path.exists(file_name):
			print("check_file_integrity(): %s doesn't exist!" % file_name)
			return False
		if os.path.getsize(file_name) != target_size:
			print("check_file_integrity(): file %s size error!" % file_name)
			return False
		return True
	else:
		ranges = split_file_size(target_size, block_count)
		for i in range(block_count):
			tmp_file_name = get_file_name_split(file_name, i)
			if not check_file_integrity(tmp_file_name, ranges[i][2], 1):
				return False
		return True


# 对各个文件块进行拼接，得到最终的文件
def append_file(file_name, block_count):
	# list 用来存放各个文件块儿
	tmp_file_name_group = []
	for i in range(block_count):
		tmp_file_name = get_file_name_split(file_name, i)
		tmp_file_name_group.append(tmp_file_name)
		# 需要事先检查要拼接的文件各个块儿是否都存在：如果发现有一块儿不存在，不拼接
		if not os.path.exists(tmp_file_name):
			return
	with open(file_name, 'wb') as out_stream:
		for tmp_file_name in tmp_file_name_group:
			with open(tmp_file_name, 'rb') as tmp_out_stream:
				out_stream.write(tmp_out_stream.read())
				os.remove(tmp_file_name)





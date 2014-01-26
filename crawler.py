#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os
import sys
import string
import datetime

import urllib.request
import urllib.error
import shutil

import logging


def download(url, file_name=None, overwrite=False):
	# 如果文件名为空，则从 URL 中获取文件名
	if file_name is None:
		file_name = url.rpartition('/')[-1]
	# 如果不覆盖己有文件，而已有文件不完整（eg. 没下载全），会有潜在影响
	if (not overwrite) and (os.path.exists(file_name)):
		return
	try:
		with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_stream:
			shutil.copyfileobj(response, out_stream)
	except urllib.error.URLError as e:
		print(e.errno, '\n', e.reason, '\n')


def GetURL(index):
	if (index in range(11, 22)) or (index >= 24):
		url = 'http://screencasts.b0.upaiyun.com/podcasts/teahour_episode_' + str(index) + '.m4a'
	elif index == 23:
		url = 'http://screencasts.b0.upaiyun.com/podcasts/teahour_episode_22-2.m4a'
	elif index == 22:
		url = 'http://teahourfm.qiniudn.com/teahour_episode_22.m4a'
	elif index == 10:
		url = 'http://screencasts.b0.upaiyun.com/podcasts/teahour_podcast_9.m4a'
	elif index == 9:
		url = 'http://screencasts.b0.upaiyun.com/podcasts/teahour_dhh.m4a'
	elif index in range(5, 9):
		url = 'http://screencasts.b0.upaiyun.com/podcasts/teahour_podcast_' + str(index) + '.m4a'
	elif index in range(2, 5):
		url = 'http://screencasts.b0.upaiyun.com/podcasts/teahour_podcast_' + str(index) + '.mp3'
	elif index == 1:
		url = 'http://screencasts.b0.upaiyun.com/podcasts/nil_podcast_1.m4a'
	return url


print('将从 Teahour.FM 下载 podcast episodes ...')
begin = int(input(u'请输入开始的期数：'))
end   = int(input(u'请输入结束的期数：'))

log_file = 'url.log'
with open(log_file, 'at') as logger:
	logger.write('\n****************************************************************************************************\n')

# 写日志到文件
logging.basicConfig(filename=log_file, format="%(asctime)s,%(msecs)d\t%(levelname)s\t%(message)s", datefmt="%Y-%m-%d %H:%M:%S", style='%', level=logging.DEBUG)
# 写日志到 stdout
stdout_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(fmt="%(asctime)s,%(msecs)d\t%(levelname)s\t%(message)s", datefmt="%Y-%m-%d %H:%M:%S", style='%')
stdout_handler.setFormatter(formatter)
logging.getLogger().addHandler(stdout_handler)

for index in range(begin, end+1):
	url = GetURL(index)
	logging.info(str(index) + '\t' + url)
	download(url)

logging.shutdown()




# URL 特征：
# 1
# http://screencasts.b0.upaiyun.com/podcasts/nil_podcast_1.m4a
# [2, 4]
# http://screencasts.b0.upaiyun.com/podcasts/teahour_podcast_2.mp3
# [5, 8]
# http://screencasts.b0.upaiyun.com/podcasts/teahour_podcast_5.m4a
# 9
# http://screencasts.b0.upaiyun.com/podcasts/teahour_dhh.m4a
# 10
# http://screencasts.b0.upaiyun.com/podcasts/teahour_podcast_9.m4a
# 下面的 URL 似乎有误？
# http://screencasts.b0.upaiyun.com/podcasts/teahour_episode_9.m4a
# 22
# http://teahourfm.qiniudn.com/teahour_episode_22.m4a
# 23
# http://screencasts.b0.upaiyun.com/podcasts/teahour_episode_22-2.m4a
# [11, 21], [24, 43]
# http://screencasts.b0.upaiyun.com/podcasts/teahour_episode_11.m4a

# download('http://screencasts.b0.upaiyun.com/podcasts/teahour_episode_43.m4a')


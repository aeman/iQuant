#!/usr/bin/python
# Filename: iQuant.py

import os,sys

DATA_PATH = './data/'
AVE_DAYS = 60

#if sys.argv[1] == "-e":

def load_data(data_file, data_list):
	try:
		f = file(data_file)
		step = 0
		for line in f.readlines():
			step = step + 1
			if step < 3: continue	#skip title
			data_list.append(line)
		f.close();
	except:
		return 0


global m_list, s_list
m_list = []; s_list = []
load_data(DATA_PATH + 'test.TXT', m_list)
load_data(DATA_PATH + 'SZ002142.TXT', s_list)

yesterday = 0.0
today = 0.0

for one_day in m_list:
	value = one_day.split('\t')
	print value[0], value[4]
	
print len(m_list)
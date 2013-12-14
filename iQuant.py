#!/usr/bin/python
# Filename: iQuant.py

import os, sys, string

DATA_PATH = './data/'
AVE_DAYS = 60

#if sys.argv[1] == "-e":

def load_market(data_file, data_list):
	try:
		f = open(data_file, "r")
		step = 0
		for line in f.readlines():
			step = step + 1
			if step < 3: continue   #skip title
			value = line.split('\t')
			data_list.append({'rq':value[0], 'kp':value[1], 'zg':value[2], 'zd':value[3], 'sp':value[4]})
		f.close();
	except IOError:
		return 0

def load_stock(data_file, data_dict):
	try:
		f = open(data_file, "r")
		step = 0
		for line in f.readlines():
			step = step + 1
			if step < 3: continue   #skip title
			value = line.split('\t')
			data_dict[value[0]] = {'kp':value[1], 'zg':value[2], 'zd':value[3], 'sp':value[4]}
		f.close();
	except IOError:
		return 0
		
def get_price(rq):
	try:
		return s_dict[rq]['sp']
	except KeyError:
		return 'no price'

global m_dict, s_dict, m_list, s_list, v_list
m_dict = {}; s_dict = {}; m_list = []; s_list = []; v_list = []

load_market(DATA_PATH + 'SH999999.TXT', m_list)
load_stock(DATA_PATH + 'SZ002142.TXT', s_dict)

days = 0; sum = 0.0

for m in m_list:
	days = days + 1;
	v_list.append(m['sp']);
	sum = sum + string.atof(m['sp'])
	print days, m['rq'], m['sp'], get_price(m['rq']),
	if days >= AVE_DAYS:
		print sum / AVE_DAYS
		sum = sum - string.atof(v_list[0])
		del v_list[0]
	else: print
	
print len(m_list)
print m_dict.keys()




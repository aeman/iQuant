#!/usr/bin/python
# Filename: iQuant.py

import os, sys, string

DATA_PATH = './data/'
MA = 30; MAVOL = 5; VOL_FAC = 1.8
INIT_MONEY = 30000.0

#if sys.argv[1] == "-e":

def load_market(data_file, data_list):
	try:
		f = open(data_file, "r")
		step = 0
		for line in f.readlines():
			step = step + 1
			if step < 3: continue   #skip title
			value = line.split('\t')
			data_list.append({'rq':value[0], 'kp':value[1], 'zg':value[2], 'zd':value[3], 'sp':value[4], 'cjl':value[5]})
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
			data_dict[value[0]] = {'kp':value[1], 'zg':value[2], 'zd':value[3], 'sp':value[4], 'cjl':value[5]}
		f.close();
	except IOError:
		return 0

def get_price(deal_date, s_type):
	try:
		return string.atof(s_dict[deal_date][s_type])   #has_key()
	except KeyError:
		return 0.0

def stock_deal(sp2, sp1, ma, kp0, deal_date, ins, cjl, mavol):
	if (sp2 <= ma and sp1 >= ma and (not ins)):
		#log.write('buy:\t%s\tsp2:%.2f\tsp1:%.2f\tma:%.2f\t\tkp0:%.2f\t\n' % (deal_date, sp2, sp1, ma, kp0))
		log.write('%.2f\t' % kp0)
		return 1
	elif ((sp2 >= ma and sp1 <= ma and ins) or (cjl / mavol > VOL_FAC and ins)):
		#log.write('sell:\t%s\tsp2:%.2f\tsp1:%.2f\tma:%.2f\t\tkp0:%.2f\t\n' % (deal_date, sp2, sp1, ma, kp0))
		log.write('%.2f\n' % kp0)
		#log.write('-------------------------------------------------------------\n')
		return -1
	else:
		#log.write('hold:\t%s\t sp2:%.2f\t sp1:%.2f\t ma:%.2f\t kp0:%.2f\t %r\n' % (deal_date, sp2, sp1, ma, kp0, ins))
		return 0


global m_dict, s_dict, m_list, s_list, p_list, v_list, all_money, in_stock, log
m_dict = {}; s_dict = {}; m_list = []; s_list = []; p_list = []; v_list = []
all_money = INIT_MONEY; in_stock = False;

#load_market(DATA_PATH + 'SH999999.TXT', m_list)
load_market(DATA_PATH + 'SZ002142.TXT', m_list)
log = open(DATA_PATH + 'deal.log', "w")

days = 0; sum_price = 0.0; sum_vol = 0; money = 0.0; ma = 0.0; mavol = 0.0

for m in m_list:
	days = days + 1;
	if days >= MA:
		#sp3 = string.atof(p_list[-3])
		sp2 = string.atof(p_list[-2])
		sp1 = string.atof(p_list[-1])
		kp0 = string.atof(m['kp'])
		cjl = string.atoi(v_list[-1])
		rst = stock_deal(sp2, sp1, ma, kp0, m['rq'], in_stock, cjl, mavol)
		if (rst != 0): in_stock = not in_stock

	p_list.append(m['sp']);   #store today's sp
	sum_price = sum_price + string.atof(m['sp'])
	v_list.append(m['cjl'])
	sum_vol = sum_vol + string.atoi(m['cjl'])
	
	if days >= MAVOL:
		mavol = sum_vol / MAVOL
		sum_vol = sum_vol - string.atoi(v_list[0])   #delete head day
		del v_list[0]
		
	if days >= MA:
		ma = sum_price / MA   #print moving average
		sum_price = sum_price - string.atof(p_list[0])   #delete head day
		del p_list[0]

log.close()

print 'iQuant OK!'

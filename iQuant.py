#!/usr/bin/python
# Filename: iQuant.py

import os, sys, string

DATA_PATH = './data/'
AVE_DAYS = 60
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

def get_price(deal_date, s_type):
	try:
		return string.atof(s_dict[deal_date][s_type])
	except KeyError:
		return 0.0

def stock_deal(sp2, sp1, ma, kp0, deal_date, ins):
	if (sp2 < ma and sp1 > ma and (not ins)):
		log.write('buy: %s -- sp2:%.2f\t sp1:%.2f\t ma:%.2f\t kp0:%.2f\t\n' % (deal_date, sp2, sp1, ma, kp0))
		return 1
	elif (sp2 > ma and sp1 < ma and ins):
		log.write('sel: %s -- sp2:%.2f\t sp1:%.2f\t ma:%.2f\t kp0:%.2f\t\n' % (deal_date, sp2, sp1, ma, kp0))
		log.write('-----------------------------------------------------\n')
		return -1
	else:
		#log.write('holding...\n');
		return 0


global m_dict, s_dict, m_list, s_list, v_list, all_money, in_stock, log
m_dict = {}; s_dict = {}; m_list = []; s_list = []; v_list = []
all_money = INIT_MONEY; in_stock = False;

load_market(DATA_PATH + 'SH999999.TXT', m_list)
load_stock(DATA_PATH + 'SZ002142.TXT', s_dict)
log = open(DATA_PATH + 'deal.log', "w")

days = 0; sum = 0.0; money = 0.0; ma = 0.0

for m in m_list:
	days = days + 1;
	if days >= AVE_DAYS:
		kp0 = get_price(m['rq'], 'kp')
		if (kp0 != 0.0):
			rst = stock_deal(string.atof(v_list[-2]), string.atof(v_list[-1]), ma, kp0, m['rq'], in_stock)
			if (rst != 0): in_stock = not in_stock

	v_list.append(m['sp']);   #store today's sp
	sum = sum + string.atof(m['sp'])
	
	if days >= AVE_DAYS:
		ma = sum / AVE_DAYS   #print moving average
		sum = sum - string.atof(v_list[0])   #delete head day
		del v_list[0]

log.close()

print 'iQuant OK!'

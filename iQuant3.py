#!/usr/bin/python
# Filename: iQuant3.py
# ÒÂ½õÒ¹ÐÐ

import os, sys, string

DATA_PATH = './data/'
INIT_MONEY = 100000.0
FIRST_MONEY = INIT_MONEY * 10000 / 223696
DEAL_YEAR = 2008

global s_list, hprice, d_price, times, all_money, all_count, s_count, in_stock, log
s_list = []; times = 0; all_money = INIT_MONEY; all_count = 0; in_stock = False;

def load_stock(data_file, data_list):
	try:
		f = open(data_file, 'r')
		step = 0
		for line in f.readlines():
			step = step + 1
			if step < 3: continue	#skip title
			value = line.split('\t')
			data_list.append({'rq':value[0], 'kp':string.atof(value[1]), 'zg':string.atof(value[2]), 'zd':string.atof(value[3]), 'sp':string.atof(value[4]), 'cjl':string.atof(value[5])})
		f.close();
	except IOError:
		return 0

def get_hprice(data_list, year):
	zg = 0.0
	for data in data_list:
		if string.atoi(data['rq'][:4]) > year:
			if zg == 0.0: return 50.0
			else: return zg / 2
		if string.atoi(data['rq'][:4]) == year and zg < data['zg']:
			zg = data['zg']

def first_buy(money, price, deal_date):
	global all_money, all_count, times, in_stock, s_count
	s_count = int(money / price)
	all_count = s_count
	all_money = all_money - price * s_count
	log.write('buy:\t%s\tprice:%.2f\tcnt:%d\n' % (deal_date, price, s_count))
	times = times + 1
	in_stock = True
	
def buy(price, deal_date):
	global all_money, all_count, times, in_stock, s_count
	s_count = s_count * 2
	all_count = all_count + s_count
	all_money = all_money - price * s_count
	log.write('buy:\t%s\tprice:%.2f\tcnt:%d\n' % (deal_date, price, s_count))
	times = times + 1
	in_stock = True
	
def sell(price, deal_date):
	global all_money, all_count, times, in_stock, hprice, d_price
	all_money = all_money + price * all_count
	log.write('sell:\t%s\tprice:%.2f\tcnt:%d\n' % (deal_date, price, all_count))
	all_count = 0
	times = 0
	in_stock = False
	hprice = hprice * 0.8
	d_price = {1:hprice, 2:hprice*0.9, 3:hprice*0.9**2, 4:hprice*0.9**3, 5:hprice*0.9**4}
	print hprice, d_price

load_stock(DATA_PATH + 'SH600036.TXT', s_list)
log = open(DATA_PATH + 'deal.log', 'w')

hprice = get_hprice(s_list, DEAL_YEAR - 1); print hprice
d_price = {1:hprice, 2:hprice*0.9, 3:hprice*0.9**2, 4:hprice*0.9**3, 5:hprice*0.9**4}
d_ratio = {1:0.045, 2:0.08, 3:0.145, 4:0.261, 5:0.469}

for s in s_list:
	if string.atoi(s['rq'][:4]) < DEAL_YEAR: continue	#ignore 2007 data
	print s['rq'], s['zg'], s['zd'], times, in_stock
	if in_stock:
		if times == 1:
			if ((s['zd'] < d_price[1] * 1.05) and (s['zg'] > d_price[1] * 1.05)):
				sell(d_price[1] * 1.05, s['rq']); continue
		else:
			if ((s['zd'] < d_price[1]) and (s['zg'] > d_price[1])):
				sell(d_price[1], s['rq']); continue
		if times == 5: continue
		else:
			if (s['zd'] < d_price[times+1]) and (s['zg'] > d_price[times + 1]):
				buy(d_price[times + 1], s['rq'])
	else:
		if (s['zd'] < d_price[1]) and (s['zg'] > d_price[1]):
			first_buy(FIRST_MONEY, d_price[1], s['rq'])

log.write('last_date:\tall_money%.2f\tall_count:%d\n' % (all_money, all_count))
log.close()

print 'iQuant OK!'

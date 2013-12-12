#!/usr/bin/python
# Filename: iQuant.py

import os,sys

DATA_PATH = './data/'

#if sys.argv[1] == "-e":
		
f = file(DATA_PATH + 'test.TXT')
for line in f.readlines():
		value = line.split('\t')
		print value[0], value[1]
f.close()

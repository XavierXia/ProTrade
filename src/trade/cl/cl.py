##!/usr/bin/python
# -*- coding:utf-8 -*-
#
#
# Copyright 2017 XavierXia(xiawenxing2010@163.com).
#
# Licensed under GNU General Public License, Version 3.0 (the "License");
import json
from pymongo import MongoClient
import sys, getopt
import pandas as pd
from pandas import Series, DataFrame
from datetime import datetime
import matplotlib.pyplot as plt

import read_conf

'''
运行方式:
	python cl.py --code=000011 --ktype=D
	python cl.py -c 000011 -k D
'''

class cl():
	def __init__(self):
		conn = MongoClient("localhost", 27017)
		self.db = conn["finance"]

		argv = sys.argv[1:]
		print "argv: ",argv

		self.code = ""
		self.ktype = ""
		try:
			opts, args = getopt.getopt(argv,"hc:k:",["help","code=","ktype="])
		except getopt.GetoptError:
			print 'python cl.py --code <gpcode> --ktype <ktype>'
			sys.exit(2)

		for opt, arg in opts:
			print "opt,arg",opt,arg
			if opt == '-h':
				print 'python cl.py --code <gpcode> --ktype <ktype>'
				sys.exit()
			elif opt in ("-c","--code"):
				self.code = arg
			elif opt in ("-k","--ktype"):
				self.ktype = arg
		print 'code: ',self.code
		print 'ktype: ',self.ktype

	def getDataFromDB(self):
		stockColl = self.db.stock
		doc = stockColl.find_one({"dCode":self.code,"dktype":self.ktype},{"dData":1,"_id":0})
		data = pd.read_json(json.dumps(doc['dData']))

		self.DFdata = data.reindex(columns=['open','high','low','close','volume'])
		self.DFdata.index = data['date']
		#print "DFdata[-20:]: ", self.DFdata[-20:]
		isDisplayMatplot = read_conf.getConfig("trade_cl", "isDisplayMatplot")
		if(int(isDisplayMatplot) == 1):
			plt.plot(self.DFdata.index, self.DFdata["close"])
			plt.show()

	def buildModel(self):
		#日线
		if self.ktype == 'D':
			dData = self.DFdata['2015-07-01':]
			print("dData[:5]: ",dData[:5])
			#寻找最小值,从最小值开始
			print("min: ", dData['low'].min())
			minIndex=dData['low'].idxmin()
			#print("minIndex: ",minIndex)
			#argMin = dData['low'].argmin()
			#print("argMin: ", argMin)
			dData = self.DFdata[minIndex:]
			print("dData[:6]: ",dData[:6])
			
			#处理包含关系



if __name__ == "__main__":
	cl = cl()
	cl.getDataFromDB()
	cl.buildModel()
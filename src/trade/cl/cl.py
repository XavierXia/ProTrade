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

import pdb
sys.path.insert(0, '/Users/xavierxia/Desktop/XavierXia/pro_code/python/ProTrade/conf/')
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

	def getParting(self):
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
			plotdat = pd.DataFrame({ "high": [], "low": [],"parting": [],"dire": [], "kcnt": [], "turn":[]})
			#row的检索
			i = 0
			#K线合并处理后的索引
			newi = 0
			#合并K线包含关系之后K线的索引,从1开始计数
			#也就是向上或向下的非包含关系的K线个数,会被重置为0
			ki = 0 

			for idx, row in dData.iterrows():
				if i == 0:
					print "idx, ", idx
					print "row, ", row
					ki += 1
					plotdat = plotdat.append(pd.DataFrame({"high": row.high,
														   "low":row.low,
														   "dire":"up",
														   "kcnt" : ki,
														   "parting": "B",
														   "turn": 1},
														   index=[idx]))
					newi += 1
					i += 1
					print "plotdat: ", plotdat
					continue
				#if i == 5:
				#	pdb.set_trace()

				if plotdat.iloc[newi-1].dire == "up": #向上合并
					if float(row.low) > float(plotdat.iloc[newi-1].low):
						if float(row.high) > float(plotdat.iloc[newi-1].high):
							ki += 1
							plotdat = plotdat.append(pd.DataFrame({"high": row.high,
									   "low":row.low,
									   "dire":"up",
									   "kcnt" : str(ki),
									   "parting": "N",
									   "turn": 0},
									   index=[idx]))
							newi += 1
						else:
							#if int(plotdat.iloc[newi-1].kcnt) == 1:
								#continue
							if int(plotdat.iloc[newi-1].kcnt) > 1: #进行包含处理
								row_index = plotdat.index[newi-1]
								plotdat.loc[row_index,'low'] = row.low
					elif float(row.low) < float(plotdat.iloc[newi-1].low):
						if float(row.high) < float(plotdat.iloc[newi-1].high):
							ki = 2
							#plotdat.iloc[newi-1].parting = "T"
							row_index = plotdat.index[newi-1]
							plotdat.loc[row_index,'parting'] = "T"
							plotdat.loc[row_index, 'turn'] = 1

							plotdat = plotdat.append(pd.DataFrame({"high": row.high,
										"low":row.low,
										"dire":"down",
										"kcnt" : str(ki),
										"parting": "N",
										"turn": 0},
										index=[idx]))
							newi += 1
						else:
							row_index = plotdat.index[newi-1]
							plotdat.loc[row_index,'high'] = row.high
					else: #两个k线最低价相等
						if float(row.high) > float(plotdat.iloc[newi-1].high):
							row_index = plotdat.index[newi-1]
							plotdat.loc[row_index,'high'] = row.high
				else: #down 向下 TODO
					if float(row.high) < float(plotdat.iloc[newi-1].high):
						if float(row.low) < float(plotdat.iloc[newi-1].low):
							ki += 1
							plotdat = plotdat.append(pd.DataFrame({"high": row.high,
									   "low":row.low,
									   "dire":"down",
									   "kcnt" : str(ki),
									   "parting": "N",
									   "turn": 0},
									   index=[idx]))
							newi += 1
						else:
							#if int(plotdat.iloc[newi-1].kcnt) == 1:
								#continue
							if int(plotdat.iloc[newi-1].kcnt) > 1: #进行包含处理
								row_index = plotdat.index[newi-1]
								plotdat.loc[row_index,'high'] = row.high

					elif float(row.high) > float(plotdat.iloc[newi-1].high):
						if float(row.low) > float(plotdat.iloc[newi-1].low):
							ki = 2

							row_index = plotdat.index[newi-1]
							plotdat.loc[row_index,'parting'] = "B"
							plotdat.loc[row_index, 'turn'] = 1

							plotdat = plotdat.append(pd.DataFrame({"high": row.high,
										"low":row.low,
										"dire":"up",
										"kcnt" : str(ki),
										"parting": "N",
										"turn": 0},
										index=[idx]))
							newi += 1
						else:							
							row_index = plotdat.index[newi-1]
							plotdat.loc[row_index,'low'] = row.low
					else: #两个k线最高价相等
						if float(row.low) < float(plotdat.iloc[newi-1].low):
							row_index = plotdat.index[newi-1]
							plotdat.loc[row_index,'low'] = row.low
				#记录循环次数
				i += 1	
			#print "plotdat[:30], ", plotdat[:30]
			print "plotdat[:], ", plotdat
			self.plotdat = plotdat
			
			isRorW = read_conf.getConfig("trade_cl", "isWriteToFileOrDB")
			if(int(isRorW) == 0):
				plotdat.to_csv("getParting.csv")


'''
	def getStroke(self):

		#划分笔
		plotStrokedat = pd.DataFrame({ "sPrice": [], "ePrice": [],"dire": [],"sDate": [], "eDate": []})
		#row的检索
		i = 0

		for idx, row in self.plotdat.iterrows():
			if i == 0:
				plotStrokedat = plotStrokedat.append(df.DataFrame({
									"sPrice": row.low,
									"ePrice": 0,
									"dire"	: "up",
									"sDate"	: idx,
									"eDate" : "0",
					}))

			#转折点
			if int(row.turn) == 1:
				if int(row.kcnt) > 4:
					pass
				elif int(row.kcnt) == 4:
					pass
				isEnergy = read_conf.getConfig("trade_cl", "kline_energy")


			i += 1
'''
	#def buildModel(self):
		#日线
		#debug
		#pdb.set_trace()
			


if __name__ == "__main__":
	cl = cl()
	cl.getDataFromDB()
	cl.getParting()
	'''cl.getStroke()'''
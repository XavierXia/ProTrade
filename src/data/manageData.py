#!/usr/bin/env python
#
#
# Copyright 2017 XavierXia(xiawenxing2010@163.com).
#
# Licensed under GNU General Public License, Version 3.0 (the "License");
'''
MongoDB stucture:
db "finance"
-----"stock"
-----------"word",like "600000","600001",...
-----------------"m","w","d","30F",...
'''
# -*- coding:utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

import tushare as ts
import json

'''
usage:
--GET
curl http://localhost:80/fetchData/600000
curl http://localhost:80/fetchData/all

TODO:
该处的接口和 处理过程均需优化,现阶段只是为了获取数据的权宜之计.
'''
class FetchDataHandler(tornado.web.RequestHandler):
	def get(self, word):
		print "FetchDataHandler: word ", word
		stockColl = self.application.db.stock
		for stock in stockColl.find():
			if stock:
				del stock['_id']
				self.write(stock)
			else:
				self.set_status(404)
				self.write({"error": "word not found"})


'''
usage:
--POST
http://localhost:80/saveData -d word=600000
http://localhost:80/saveData -d word=all
'''
class SaveDataHandler(tornado.web.RequestHandler):
	def post(self):
		stockColl = self.application.db.stock
		word = self.get_argument('word','')
		if word == '':
			self.write('Please again input!')

		dD = ts.get_k_data(str(word))
		dD = json.loads(dD.to_json(orient='records'))
		#f30D = ts.get_k_data(str(word),ktype='30')
		#f30D = json.loads(f30D.to_json(orient='records'))

		#astock = {str(word):{'d':dD,'30F':f30D}}
		astock = {str(word):{'d':dD}}
		#self.write(astock)

		stockColl.save(astock)
		del astock['_id']
		self.write(astock)



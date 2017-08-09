#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#
# Copyright 2017 XavierXia(xiawenxing2010@163.com).
#
# Licensed under GNU General Public License, Version 3.0 (the "License");

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
		word = self.get_argument('word','default')
		if word == 'default':
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

'''
http://localhost/md?ac=save&tp=stock&cd=600000

'''
class ManageDataHandler(tornado.web.RequestHandler):
	def get(self,word):
		args = self.request.arguments
		arg1 = self.get_arguments("tp")
		data = self.request.query_arguments
		#TODO error
		logger = self.application.logger
		#arg2 = self.get_query_arguments()
		#code = args[2]
		logger.info("arg1....%s",args)
		logger.info("arg2....%s",arg1)
		logger.info("data....%s",data)
		self.write({"hao":"111"})
		'''
		dD = ts.get_k_data(str(code))
		dD = json.loads(dD.to_json(orient='records'))

		stockColl = self.application.db.stock
		sDoc = stockColl.findOne({"dCode":code})
		if sDoc:
			stockColl.update({"dCode":code},{"$push":code})
		else:
			stockColl.insert({"dCode":code})
			stockColl.update({"dCode":code},{"$push":{"dData":dD}})
		del stockColl["_id"]
		self.write(stockColl)
		'''
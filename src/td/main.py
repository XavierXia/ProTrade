#!/usr/bin/env python
#
#
# Copyright 2017 XavierXia(xiawenxing2010@163.com).
#
# Licensed under GNU General Public License, Version 3.0 (the "License");

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from pymongo import MongoClient

from tornado.options import define, options

import logging
import sys
sys.path.insert(0, '/Users/hebo/Desktop/XavierXia/pro_code/python/ProTrade/conf/')
sys.path.append('../')
from data.manageData import *

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [(r'/md', ManageDataHandler)
		]
		conn = MongoClient("localhost", 27017)
		self.db = conn["finance"]

		#TODO error
		logging.config.fileConfig("/Users/hebo/Desktop/XavierXia/pro_code/python/ProTrade/conf/logging.conf")
		self.logger = logging.getLogger("example01")

		tornado.web.Application.__init__(self, handlers, debug=True)
		self.logger.debug("This is debug message")
		self.logger.info("This is info message")
		self.logger.warning("This is warning message")

if __name__ == "__main__":
	#upper log level
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

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
import pymongo

from tornado.options import define, options

import sys
sys.path.append('../')
from data.manageData import *

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [(r'/fetchData/(\d+)', FetchDataHandler),
					(r'/saveData', SaveDataHandler)
		]
		conn = pymongo.Connection("localhost", 27017)
		self.db = conn["finance"]
		tornado.web.Application.__init__(self, handlers, debug=True)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print('http://localhost:8000, main.py')
    tornado.ioloop.IOLoop.instance().start()

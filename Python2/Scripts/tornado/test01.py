#!/bin/env python2.7

import os.path
import json
from collections import defaultdict
#from zmq.eventloop import ioloop

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


valDict = defaultdict(lambda: defaultdict(list))


class indexHandler(tornado.web.RequestHandler):
    def head(self):
        self.set_header('Task-Ids',len(valDict))


class listHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({k:1 for k in valDict.keys()})
            
                   
class gdHandler(tornado.web.RequestHandler):
    def get(self,key):
        self.write(valDict.get(key,{}))
            
                   
class sdHandler(tornado.web.RequestHandler):
    def post(self,key):
        for arg_key in self.request.arguments.keys():
            valDict[key][arg_key] += self.get_arguments(arg_key)

            
app = tornado.web.Application(
    handlers=[
        (r"/", indexHandler),
        (r"/list", listHandler),
        (r"/getData/(\w+)", gdHandler),
        (r"/saveData/(\w+)", sdHandler),
    ],
)

def main():
    #ioloop.install()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
# end def


if __name__ == "__main__":
    main()

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
        pass


class listHandler(tornado.web.RequestHandler):
    def head(self):
        self.set_header('Task-Ids',len(valDict.keys()))

    def get(self):
        self.write({k:1 for k in valDict.keys()})
            
                   
class dataHandler(tornado.web.RequestHandler):
    def head(self,key):
        self.set_header('Task-Id',key)
        self.set_header('Task-Id-Exists', key in valDict)

    def get(self,key):
        self.write(valDict.get(key,{}))

    def post(self,key):
        for arg_key in self.request.arguments.keys():
            valDict[key][arg_key] += self.get_arguments(arg_key)
            
                   
app = tornado.web.Application(
    handlers=[
        (r"/", indexHandler),
        (r"/data", listHandler),
        (r"/data/(\w+)", dataHandler),
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

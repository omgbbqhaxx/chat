#!/usr/bin/env python
import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.wsgi
from chatsocial.wsgi import application as wsgi_handler 

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("index.html").generate())

class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print 'connection opened...'
    self.write_message("The server says: 'Hello'. Connection was accepted.")

  def on_message(self, message):
    self.write_message("The server says: " + message + " back at you")
    print 'received:', message

  def on_close(self):
    print 'connection closed...'
def main():
    wsgi_app = tornado.wsgi.WSGIContainer(wsgi_handler)
    application = tornado.web.Application([
      (r'/ws', WSHandler),
      (r'/', MainHandler),
      ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
      (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
    ])
    server = tornado.httpserver.HTTPServer(application)
    server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()



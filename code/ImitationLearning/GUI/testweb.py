import tornado.ioloop
import tornado.web
import os
from GUI.playhandler import PlayHandler
from GUI.musiccontrolhandler import MusicControlHandler
from GUI.actioncontrolhandler import ActionControlHandler
from GUI.midicontrolhandler import MidiControlHandler
from api.engineapi import EngineAPI
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class MusicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("musiclearning.html")

class MidiHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("midilearning.html")       

class PianoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("piano.html")
               
settings = {"static_path" : os.path.join(os.path.dirname(__file__),"static")}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/action",ActionControlHandler),
    (r"/play",PlayHandler),
    (r"/musiccontrol",MusicControlHandler),
    (r"/midicontrol",MidiControlHandler),
    (r"/musiclearning.html",MusicHandler),
    (r"/piano.html",PianoHandler),
    (r"/midilearning.html",MidiHandler)],**settings
)
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
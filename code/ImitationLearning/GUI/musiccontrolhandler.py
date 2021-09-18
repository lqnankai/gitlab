'''
Created on 2016.7.6

@author: liangqian
'''
import tornado.web
from GUI.globaldata import brainEngine
import datetime
class MusicControlHandler(tornado.web.RequestHandler):
    '''
    classdocs
    '''
    def get(self):
        
        notes = self.get_argument("action")
        musicName = self.get_argument("name")
        intervals = self.get_argument("interval")
        jstr = brainEngine.rememberNotes(musicName, notes,intervals)
        #self.write(jstr)
'''
Created on 2016.7.20

@author: liangqian
'''
import tornado.web
class ActionControlHandler(tornado.web.RequestHandler):
    '''
    classdocs
    '''


    def get(self):
        l = self.get_arguments("")
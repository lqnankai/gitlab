'''
Created on 2016.4.8

@author: liangqian
'''
#from __builtin__ import False

class Izhikevich():
    '''
    classdocs
    '''


    def __init__(self, a,b,c,d,vthresh):
        '''
        Constructor
        '''
        self.type = 'exc'
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.I = 0
        self.v = -65
        self.u = b * self.v
        self.vthresh = vthresh
        self.spike = False
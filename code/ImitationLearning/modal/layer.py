'''
Created on 2016.6.12

@author: liangqian
'''
from abc import ABCMeta,abstractmethod
class Layer():
    '''
    classdocs
    '''
    _metaclass_ = ABCMeta

    def __init__(self):
        '''
        Constructor
        '''
        self.neutype = ''
        self.groups = {}
    
    @ abstractmethod
    def resetProperties(self):
        raise NotImplementedError
    
    def addNewGroups(self,layerID,neunum):
        raise NotImplementedError
        
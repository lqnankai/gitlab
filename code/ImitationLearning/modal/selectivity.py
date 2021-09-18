'''
Created on 2016.7.6

@author: liangqian
'''
from abc import ABCMeta,abstractmethod
class Selectivity():
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def setNeuronSelectivity(self,begin,end):
        pass


class DirectionSelectivity(Selectivity):
    
    @abstractmethod
    def setNeuronSelectivity(self, begin, end):
        pass
'''
Created on 2016.4.22

@author: liangqian
'''

class GaussianNeuron():
    '''
    This class is used to define the Gaussian neuron to express the object
    
    '''


    def __init__(self,I_min = 0,I_max = 15,beta = 0.1):
        '''
        Constructor
        '''
        self.beta = beta
        self.I_min = I_min
        self.I_max = I_max
        self.center_ReceptiveField = 0
        self.index = -1
        self.variance = 0
        
    def computeProperties(self,M):
        
        self.center_ReceptiveField = self.I_min + (self.index - 1) * (self.I_max - self.I_min)/(M-2)
        self.variance = self.beta * (self.I_max - self.I_min)/(M-2)
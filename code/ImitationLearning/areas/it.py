'''
Created on 2016.4.14

@author: liangqian
'''
from modal.cluster import *
from data.ventrovision import *
import math
import numpy as np

class IT():
    '''
    This area is used to encoding the object with neural cluster and generate spike trains to
    express the object
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.spikeTrains = {} #key:neuron index, value:spike time
        self.clusters = []
        self.num = 20
    
    def createNetwork(self):
        for i in range(0,dimention):
            c = Cluster('Gaussian',self.num)
            c.createClustersNetwork()
            self.clusters.append(c)
    
    def generateGussianTrains(self,objectName):
        
        # compute the Gaussian receptive field
        for c in self.clusters:
            for node in c.neurons:
                node.computeProperties(self.num)
        
        # output spike trains
        for i in range(0,objectName.shape[0]):
            #print('*'*5+'I am a border'+'*'*5)
            v = objectName[i]
            for n in self.clusters[i].neurons:
                t = math.exp(-1 * (v - n.center_ReceptiveField)**2/2 * n.variance)
                # 0.01 as the time step
                t = int(t/0.01)
                self.spikeTrains[i*50 + n.index] = t
            
'''
Created on 2016.6.12

@author: liangqian
'''
from modal.cluster import Cluster
from modal.layer import Layer
from modal.ipscluster import IPSCluster
class GoalLayer(Layer):
    '''
    classdocs
    '''


    def __init__(self, neutype = 'LIF'):
        '''
        Constructor
        '''
        self.neutype = neutype
        self.groups = {}
    
    def setTestStates(self):
        for id,g in self.groups.items():
            g.setTestStates()
    
    def addNewGroups(self, groupID, layerID,neunum,goalname):
        
        g = IPSCluster(self.neutype,neunum)
        g.id = groupID
        g.name = goalname
        g.createClusterNetwork()
        g.setPropertiesofNeurons(groupID, 'G', layerID)
        self.groups[goalname] = g
        
        
        
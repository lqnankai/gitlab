'''
Created on 2016.4.12

@author: liangqian
'''
from modal.cluster import Cluster
from modal.goallayer import GoalLayer

class PFC():
    '''
    PFC is used to make decision 
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.goallayers = {}
        
    def createGoalLayers(self,layernum,neutype,neunumpergroup):
        for i in layernum:
            gl = GoalLayer(neutype)
            self.goallayers[i+1] = gl
            
    def addNewGoal(self,layerNum):
        gl = self.goallayers.get(layerNum)
        gl.addNewGroups(len(gl),20)
        
            
        
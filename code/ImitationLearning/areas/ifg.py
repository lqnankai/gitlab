'''
Created on 2016.6.21

@author: liangqian
'''
from modal.cluster import Cluster
from modal.goallayer import GoalLayer

class IFG():
    '''
    classdocs
    '''


    def __init__(self, params):
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
        gl.addNewGroups(len(gl.groups),20)
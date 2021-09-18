'''
Created on 2016.5.24

@author: liangqian
'''
from modal.joint import Joint
class Action():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.joints = []
        
    def setJoints(self,data):
        
        for i in range(0,25):
            jj = Joint()
            value = data.get(str(i))
            jj.setCoordinate(value)
            self.joints.append(jj)
            
'''
Created on 2016.4.26

@author: liangqian
'''
class Brodomman_7():
    '''
    This file is used to encoding the positions of the joints
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    
    def readJointsData(self):
        
        f = open('Data.txt')
        while(1):
            line = f.readline()
            if(len(line) != 0):# line is not empty
                
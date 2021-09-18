'''
Created on 2016.5.24

@author: liangqian
'''
import math
class Joint():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.x = 0
        self.y = 0
        self.z = 0
        self.x_o = 0
        self.y_o = 0
        self.z_o = 0
        self.v_len = 0
        
        
    def setCoordinate(self,data):
        x = round(float(data.get('X')),3)
        y = round(float(data.get('Y')),3)
        z = round(float(data.get('Z')),3)
        veclen = math.sqrt(x**2+y**2+z**2)
        self.x_o = x
        self.y_o = y
        self.z_o = z
        self.v_len = veclen
        self.x = round(math.acos(x/veclen),3) # angle of x axe
        self.y = round(math.acos(y/veclen),3) # angle of y axe
        self.z = round(math.acos(z/veclen),3) # angle of z axe
        
        
'''
Created on 2016.4.14

@author: liangqian
'''
'''
This file is used to store the information of ventrovisual pathway
'''
# transform the word to a vector of 16 dimentions
import random
import numpy as np
min = 0
max = 15
dimention = 4

#--------------------- object -------------------------#
_CUP = np.random.uniform(min,max,size = dimention)
_PHONE = np.random.uniform(min,max,size = dimention)




#----------------------joint---------------------------#
_SpineBase    = 0,
_SpineMid    = 1,
_Neck    = 2,
_Head    = 3,
_ShoulderLeft    = 4,
_ElbowLeft    = 5,
_WristLeft    = 6,
_HandLeft    = 7,
_ShoulderRight    = 8,
_ElbowRight    = 9,
_WristRight    = 10,
_HandRight    = 11,
_HipLeft    = 12,
_KneeLeft    = 13,
_AnkleLeft    = 14,
_FootLeft    = 15,
_HipRight    = 16,
_KneeRight    = 17,
_AnkleRight    = 18,
_FootRight    = 19,
_SpineShoulder    = 20,
_HandTipLeft    = 21,
_ThumbLeft    = 22,
_HandTipRight    = 23,
_ThumbRight    = 24
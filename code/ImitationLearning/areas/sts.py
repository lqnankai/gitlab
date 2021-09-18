'''
Created on 2016.4.8

@author: liangqian
'''
from modal import *
from modal.action import Action
from modal.joint import Joint
from modal.cluster import Cluster
from tools.readjson import *
class STS():
    '''
    STS is used for encoding visual action,including joints and their angles
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        self.cluster = Cluster('Gaussian',25) # a neuron is corresponding to a human joint
        self.actions = [] # action sequence
    
    def getActions(self):
        jdata = readjsonFile('./task1/task1_line1/kinect.txt')
        for i in range(1,len(jdata)+1):
            value = jdata.get(str(i))
            act = Action()
            act.setJoints(value)
            self.actions.append(act)
            

# s = STS()
# s.getActions()
# fs = []
# for i in range(0,25):
#     f = open('../output/'+str(i)+'.csv','w')
#     f.write('T,xo,yo,zo,vlen,x,y,z\n')
#     fs.append(f)
# 
# for t in range(0,len(s.actions)):
#     act = s.actions[t]
#     for i in range(0,len(act.joints)):
#         jj = act.joints[i]
#         strs = str(t)+','+str(jj.x_o)+','+str(jj.y_o)+','+str(jj.z_o)+','+str(jj.v_len)+','+str(jj.x)+','+str(jj.y)+','+str(jj.z)+'\n'
#         f = fs[i]
#         f.write(strs)
# 
# for i in range(0,25):
#     f.close()

'''
Created on 2016.4.19

@author: liangqian
'''
#from tools.generateData import *
import numpy as np
#import pylab as pl
from modal.directionsequencelayer import DirectionSequenceLayer
from modal.sequencememory import SequenceMemory
class Action_Sequence_Mem(SequenceMemory):
    '''
    This class stores the action sequences
    This memory is a hierarchy model
    '''


    def __init__(self,neutype = 'LIF'):
        '''
        Constructor
        '''
        SequenceMemory.__init__(self, neutype)
    
    def createActionSequenceMem(self,layernum,neutype,neunumpergroup):
        
        # try to create sequence layer and goal layer
        sl = DirectionSequenceLayer(neutype)
        self.sequenceLayers[len(self.sequenceLayers) + 1] = sl
        
        
        
    
    def doRemembering(self,act,order,dt,t):
        sl = self.sequenceLayers.get(1)
#         sl.addNewGroups(GroupID = order,layerID = 1,neunum = 16)
        group = sl.groups.get(order)
        dt = 0.1
        for n in group.neurons:
            n.I_ext = act.joints[11].x
            n.computeFilterCurrent()
            n.update(dt,t,'Learn')
            
    
#     def doConnectToGoal(self,goal,order): # connect to the goal in the time window
#         
#         sl = self.sequenceLayers.get(1)
#         group = sl.groups.get(order)
#         
#         # the goal and the group always generate spikes in a limit time window,create a synapse between them.
#         tb = (order-1)*group.timeWindow
#         te = order * group.timeWindow
#         sp1_goal = {}
#         sp2 = []
#         
#         for n in goal.neurons:
#             sp = []
#             for st in n.spiketime:
#                 if(st < te and st >= tb ):
#                     sp.append(st)
#             sp1_goal[n.index] = sp
#         
#         for n in group.neurons:
#             if(len(n.spiketime) > 0):
#                 for index,sp in sp1_goal.items():
#                     temp = 0
#                     for sp1 in n.spiketime: #spike times of group
#                         for sp2 in sp:
#                             if(abs(sp1-sp2) <= n.tau_ref):
#                                 temp += 1
#                     if(temp >= 4): # super threshold, create a new synapse between goal and neurons of sequence group
#                         syn = Synapse(goal.neurons[index-1],n)
#                         syn.type = 2
#                         syn.weight = 3
#                         n.pre_neurons.append(goal.neurons[index-1])
#                         n.synapses.append(syn)
#                                
#                 
#                         
#         
#         
#             
#     def setTestStates(self):
#         for lid,sl in self.sequenceLayers.items():
#             sl.setTestStates()
#             
#     def doRecalling_old(self):
#         sl = self.sequenceLayers.get(1)
#         dt = 0.1
#         time = np.arange(0,len(sl.groups)*5,dt)
#         output = np.zeros(len(time))
#         for gid,group in sl.groups.items():
#             firstspikeNeuron = 0
#             flag = False
#             for i in range((gid-1)*int(group.timeWindow/dt),gid*int(group.timeWindow/dt)):
#                 t = time[i]
#                 for n in group.neurons:
#                     n.update(dt,t,'test')
#                     if(n.spike == True and flag == False):
#                         firstspikeNeuron = n.index
#                         flag = True
#                     if(flag == True):
#                         output[i] = firstspikeNeuron
#         
#         pl.plot(time,output)
#         pl.show()
    
        
        
                              
                        
                    
                    
                   
# asm = Action_Sequence_Mem()
# asm.createActionSequenceMem(layernum=2,neutype= 'LIF',neunumpergroup=16)
# layer2 = asm.layers.get(2)
# for key,group in layer2.items():
#     print('group: ' +str(group.id))
#     for n in group.neurons:
#         print('current neuron: ' + str(n.index))
#         print('pre_synaptic neurons:')
#         for syn in n.synapses:
#             print('synapse type: ' + str(syn.type)) 
#             print(syn.pre.index)
#             print(syn.pre.groupIndex)      
#     print('\n')


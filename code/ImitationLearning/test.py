'''
Created on 2016.4.8

@author: liangqian
'''
from data.ventrovision import _PHONE
from modal.cluster import Cluster
from areas.it import IT
from areas.sts import STS
from areas.ips import IPS
from areas.memory.action_sequence_mem import Action_Sequence_Mem
import numpy as np
import pylab as pl
import random
import math
if __name__ == '__main__':
    '''
    test Gaussian encoding
    '''
#     area_STS = STS()
#     area_STS.cluster.createNetwork()
#     print(area_STS.cluster.neurons)
    
#     area_IT = IT()
#     area_IT.createNetwork()
#     print(_PHONE)
#     area_IT.generateGussianTrains(_PHONE)
    
    '''
    test activity of a cluster
    '''
#     c = Cluster('LIF',neunum=10)
#     c.createClusterNetwork()
#     c.setInhibitoryNeurons(0.2)
#     c.createFullConnections()
#     
#     T = 10
#     dt = 0.1
#     step = int(T/dt)
#     time = np.arange(0,T,dt)
#     tt = np.arange(0,step)
#     spikepoint = [[] for i in range(0,10)]
#     for i in range(0,len(time)):
#         #print ('T=' + str(t))
#         t = time[i]
#         for neu in c.neurons:
#             #print(neu.index)
#             neu.update(dt,t)
#             if(neu.spike == 1):
#                 spikepoint[neu.index].append(neu.index)
#             else:
#                 spikepoint[neu.index].append(0)
#     
#     print(len(c.neurons[1].spiketime))
#     pl.subplot(1,1,1)
#     for i in range(10):
#         pl.scatter(time,spikepoint[i],marker = '.')
#     pl.show()

    neuron_type = 'LIF'
    area_STS = STS()
    area_STS.getActions()
    area_IPS = IPS(neuron_type)
    
    
    area_IPS.addNewSubGoal('1')
    asm = Action_Sequence_Mem()
    asm.createActionSequenceMem(2, neuron_type, 120)
    
    dt = 0.1
    time = np.arange(0,len(area_STS.actions) * 5,dt)
    
    for order,act in enumerate(area_STS.actions):         
        sl = asm.sequenceLayers.get(1)
        sl.addNewGroups(GroupID = order+1,layerID = 1,neunum = 120) # add a new event of a sequence
        
        for t in time[int(order*5/0.1):int((order+1)*5/0.1)]:
            area_IPS.doRemebering('1',dt,t)
            asm.doRemembering(act,order+1,dt,t)        
        asm.doConnectToGoal(area_IPS.goals.groups.get('1'),order+1)
        
        # plot for debug
#         for i,n in enumerate(asm.sequenceLayers.get(1).groups.get(order+1).neurons):
#             sp = []
#             for t in time[order*5/0.1:(order+1)*5/0.1]:
#                 if(t in n.spiketime):
#                     sp.append(1)
#                 else:sp.append(0)
#             print(len(time[order*5/0.1:(order+1)*5/0.1]))
#             print(len(sp))
#             pl.subplot(4,4,i+1)
#             pl.plot(time[order*5/0.1:(order+1)*5/0.1],sp)
#             pl.title('n=' + str(n.index))
#         pl.show()
    
    area_IPS.setTestStates()
    asm.setTestStates()
    result = area_IPS.doRecalling('1',asm)
    print(result)
    time = np.arange(1,len(result)+1,1)
    resultData = []
    originalData = []
    for i,act in enumerate(area_STS.actions):
        j = act.joints[11]
        originalData.append(j.x)
        value = result.get(i+1)
        v = random.uniform(value-math.pi/240,value+math.pi/240)
        resultData.append(v)
        
    print(originalData)
    print(resultData)
    pl.plot(time,originalData)
    pl.plot(time,resultData)
    pl.axis([1,5,0,2])
    pl.show()
    
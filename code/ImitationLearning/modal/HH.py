'''
Created on 2016.5.11

@author: liangqian
'''
import math
import random
import numpy as np
#import pylab as pl
from modal.synapse import Synapse
class HHNeuron():
    '''
    This file is used to define the HH neural modal
    '''


    def __init__(self,type = 'exc'):
        '''
        Constructor
        '''
        self.type = type #excited neuron:exc, inhibited neuron: inh
        self.layerIndex = 0 # the layer in which the neuron situated
        self.groupIndex = 0 # the group in which the neuron situated
        self.index = 0
        self.timewindow = 200 # time window
        self.v = 0
        self.I_ext = 40
        self.I_rest = -10
        self.I_syn_lower = 0
        self.I_syn_upper = 0
        self.I_ion = 0
        self.v_rest = 0
        self.v_thresh = 10
        self.Am = 0
        self.Ah = 0
        self.An = 0
        self.Bm = 0
        self.Bh = 0
        self.Bn = 0
        self.gNa = 120 * (1+0.02*random.uniform(-1,1))
        self.gk = 36 * (1+0.02*random.uniform(-1,1))
        self.gL = 0.3 * (1+0.02*random.uniform(-1,1))
        self.m = 0
        self.h = 0
        self.n = 0
        self.spike = 0
        self.spiketime = []
        self.pre_neurons = []
        self.synapses = [] # this neuron is used as post_synaptic neuron
        self.synapses_pre = [] #this neuron is used as pre_synaptic neuron
    
    def update(self,dt,t):
        
        if(t == 6.5 and self.index == 2):
            print('debug')
        self.spike = 0
        self.updateSynapses(t)
        self.updateCurrentOfLowerAndUpperLayer(t)
        if(self.v >= 55):
            self.v = 0
            self.spike = 1
            self.spiketime.append(t)
            #print('neuron ' +str(self.index) +' fires')
        else:
            self.v += dt * (-self.I_ion + self.I_syn_lower + self.I_syn_upper + self.I_ext)
            self.m = dt * (self.Am * (1-self.m) - self.Bm * self.m)
            self.h = dt * (self.Ah * (1-self.h) - self.Bh * self.h)
            self.n = dt * (self.An * (1-self.n) - self.Bn * self.n)
            
            print(t)
            print(self.index)
            print(self.v)
            self.Am = (2.5-0.1*(self.v - self.v_rest))/(math.exp(2.5-0.1*(self.v - self.v_rest))-1)
            self.Bm = 4 * math.exp(-(self.v-self.v_rest)/18.0)
            self.Ah = 0.07 * math.exp(-(self.v-self.v_rest)/20.0)
            self.Bh = 1/(math.exp(3-0.1*(self.v-self.v_rest))+1)
            self.An = (0.1-0.01*(self.v-self.v_rest))/(math.exp(1-0.1*(self.v-self.v_rest))-1)
            self.Bn = 0.125*math.exp(-(self.v-self.v_rest)/80.0)
        
        self.I_ion = self.gNa * self.m*self.m*self.m*self.h*(self.v-50)+self.gk*self.n*self.n*self.n*self.n*(self.v+77)+self.gL*(self.v+54.4)
    
    def updateSynapses(self,t):
        for syn in self.synapses:
            syn.computeWeight(t) 
    
    def updateCurrentOfLowerAndUpperLayer(self,t):
        I_inh = 0
        I_ext = 0
        I_exc_ext = 0
        for syn in self.synapses:
            # compute the alpha value of all spikes before this time t
            alpha_value = 0
            for st in syn.pre.spiketime:
                temp = 0
                if(t - st >= 0): temp = 0.6*(t/1000)*math.exp(-0.03*(t - st)/1000)
                else:temp = 0
                alpha_value += temp
            if(syn.type == 0): # from the same group
                if(syn.pre.type == 'inh'):
                    I_inh += syn.weight * (self.v+80) * alpha_value
                if(syn.pre.type == 'exc'):
                    I_ext += syn.weight * self.v * alpha_value
            if(syn.type == 1):# from other modules in the same layer
                I_exc_ext += syn.weight * self.v * alpha_value
            if(syn.type == 2): # from the upper layer
                self.I_syn_upper += self.weight * self.v * alpha_value
                
        self.I_syn_lower = -I_inh + I_ext + I_exc_ext
        
        #print(self.I_syn_lower)

# neu = HHNeuron()
# dt = 0.05
# T = 100
# step = int(T/dt)
# time = np.arange(0,T,dt)
# spike = np.zeros(step)
# for i in range(0,step):
#     neu.update(dt,i)
#     spike[i] = neu.v
# pl.subplot(1,1,1)       
# pl.plot(time,spike)
# pl.show()

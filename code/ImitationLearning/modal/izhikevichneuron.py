'''
Created on 2016.4.8

@author: liangqian
'''
from modal.izhikevich import Izhikevich
import math
import numpy as np
import pylab as pl
class IzhikevichNeuron(Izhikevich):
    '''
    classdocs
    '''


    def __init__(self, a = 0.5,b = 0.2,c = -65,d = 2,vthresh = 30):
        '''
        Constructor
        '''
        Izhikevich.__init__(self, a, b, c, d, vthresh)
        self.synapses = [] #this neuron is considered as post-synaptic neuron
        self.spiketime = []
        self.pre_neurons = []
        self.I_syn_lower = 0
        self.I_syn_upper = 0
        self.I_ext = 63.5
        
    def update(self,dt,t):
        
        self.spike = 0
        self.updateSynapses(t)
        self.updateCurrentOfLowerAndUpperLayer(t)
        self.I = self.I_ext + self.I_syn_lower + self.I_syn_upper
        self.v += dt * (0.04*self.v * self.v + 5 * self.v + 140 - self.u + self.I)
        self.u += dt * self.a * (self.b *self.v - self.u)
        #self.synapseWeightsDepression()
        
        if(self.v >= 30):
            self.spike = 1
            self.v = self.c
            self.u += self.d
            self.spiketime.append(t)
        
        
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
                if(t - st >= 0): temp = 6*(t/1000)*math.exp(-0.03*(t - st)/1000)
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
        
# neu = IzhikevichNeuron(a = 0.01,b=0.2,c=-65,d=8)
# dt = 0.1
# T = 1000
# step = int(T/dt)
# time = np.arange(0,T,dt)
# spike = np.zeros(step)
# for i in range(0,step):
#     neu.update(dt,time[i])
#     spike[i] = neu.v
# print(len(neu.spiketime))
# pl.subplot(1,1,1)       
# pl.plot(time,spike)
# pl.show()
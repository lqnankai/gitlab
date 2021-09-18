'''
Created on 2020/10/03

@author: liangqian
'''
from modal.lifneuron import LIFNeuron
class ComposerLIFNeuron(LIFNeuron):
    '''
    classdocs
    '''


    def __init__(self, tau_ref = 0.5,vthresh = 5,Rm = 2,Cm = 0.2):
        '''
        Constructor
        '''
        LIFNeuron.__init__(self, tau_ref, vthresh, Rm, Cm)
        
    def update(self,dt,t):
        self.spike = False
        #self.updateCurrentOfLowerAndUpperLayer(t)
        if(t >= self.t_rest):
            self.v += dt * (-self.v + self.I * self.Rm) / self.tau_m
            if(self.v > self.vth):
                self.spike = True
                self.spiketime.append(t)
                self.v = 0
                self.t_rest = t + self.tau_ref
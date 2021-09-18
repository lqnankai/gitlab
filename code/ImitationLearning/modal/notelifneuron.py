'''
Created on 2016.7.6

@author: liangqian
'''
from modal.lifneuron import LIFNeuron
class NoteLIFNeuron(LIFNeuron):
    '''
    classdocs
    '''


    def __init__(self,tau_ref = 0.5,vthresh = 5,Rm = 2,Cm = 0.2):
        '''
        Constructor
        '''
        LIFNeuron.__init__(self, tau_ref, vthresh, Rm, Cm)
        
    def setPreference(self):
        self.selectivity = self.index-2
    
    def computeFilterCurrent(self):
        if(self.I_ext == self.selectivity):
            self.I = 10
        
    def updateCurrentOfLowerAndUpperLayer(self,t):
        self.I_lower = 0
        self.I_upper = 0
        for syn in self.synapses:
            syn.computeShortTermFacilitation(t)
            if(syn.type == 0) :  # the same group
                if(syn.excitability == 0):
                    self.I_lower -= syn.weight * syn.strength
                    if(self.I_lower < -20):self.I_lower = -20
            if(syn.type == 1) : # pre and post neurons come from  the same layer but not the same group
#                 if(syn.weight > 0):
#                     print('pre_neuron_group id:'+str(syn.pre.groupIndex) + ' neuron index:'+str(syn.pre.index))
#                     print('post_neuron_group id:'+str(self.groupIndex) + ' neuron index:'+str(self.index))
#                     print(syn.weight)
                self.I_lower += syn.weight * syn.strength
                #print('syn.strength='+str(syn.strength))
                
            if(syn.type == 2) :  #pre and post neurons come from the different layers
                #print(syn.pre.groupIndex)
                self.I_upper += syn.weight * syn.strength
        
#         if(self.I_upper == 0):
#             self.I = self.I_ext   
        else:self.I = self.I_lower + self.I_upper
        
'''
Created on 2016.4.8

@author: liangqian
'''

class LIF():
    '''
    classdocs
    '''


    def __init__(self, tau_ref,vthresh,Rm,Cm):
        '''
        Constructor
        '''
        self.type = 'exc'
        self.tau_ref = tau_ref
        self.vth = vthresh
        self.Rm = Rm
        self.Cm = Cm
        self.tau_m = self.Rm * self.Cm
        self.t_rest = 0
        self.v = 0
        self.I = 0
        self.spike = False
        self.firingrate = 0 # Hz
        
    
        
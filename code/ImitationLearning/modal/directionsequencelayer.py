'''
Created on 2016.7.6

@author: liangqian
'''
from modal.sequencelayer import SequenceLayer
from modal.directioncluster import DirectionCluster
from modal.synapse import Synapse
class DirectionSequenceLayer(SequenceLayer):
    '''
    classdocs
    '''


    def __init__(self, neutype):
        '''
        Constructor
        '''
        SequenceLayer.__init__(self,neutype)
        
    def addNewGroups(self, GroupID, layerID, neunum):
        g = DirectionCluster(self.neutype,neunum)
        g.createClusterNetwork()
        g.id = GroupID
        g.setPropertiesofNeurons(g.id, 'S',layerID)
        self.groups[g.id] = g
        
        #create full connection with the former group
        if(len(self.groups) > 1):
            for i in range(1,g.id)[::-1]:
                pre_g = self.groups.get(i)
                for n1 in pre_g.neurons:
                    for n2 in g.neurons:
                        if(n1.type == 'inh' or n2.type == 'inh'):continue;
                        syn = Synapse(n1,n2)
                        syn.type = 1
                        syn.delay = g.id - pre_g.id
                        n2.pre_neurons.append(n1)
                        n2.synapses.append(syn)
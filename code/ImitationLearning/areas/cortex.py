'''
Created on 2016.7.6

@author: liangqian
'''
from conf.conf import *
from data.ventrovision import _PHONE
from modal.cluster import Cluster
from areas.it import IT
from areas.sts import STS
from areas.ips import IPS
from areas.memory.action_sequence_mem import Action_Sequence_Mem
from areas.memory.music_sequence_mem import Music_Sequence_Mem
from areas.apac import APAC
import random
import numpy as np
class Cortex():
    '''
    This class is used to control areas in the cortex, just cortex controlling
    '''
    
    def __init__(self,neutype,dt):
        self.neutype = neutype
        self.asm = Action_Sequence_Mem(neutype)
        self.msm = Music_Sequence_Mem(neutype)
        self.ips = IPS(self.neutype)
        self.apac = APAC()
        self.dt = dt
        
    
        
    def addSubGoalToIPS(self,goalname):
        self.ips.addNewSubGoal(goalname)
        tt = np.arange(0,5,self.dt)
        for t in tt:
            self.ips.doRemebering(goalname, self.dt, t)
            
    def addComposerToIPS(self,composername):
        self.ips.addNewComposer(composername)
        tt = np.arange(0,5,self.dt)
        for t in tt:
            self.ips.doRememberingComposer(composername, self.dt,t)
    
    def addGenreToIPS(self,genrename):
        self.ips.addNewGenre(genrename)
        tt = np.arange(0,5,self.dt)
        for t in tt:
            self.ips.doRememberingGenre(genrename, self.dt,t)
            
            
    def musicSequenceMemroyInit(self):
        self.msm.createActionSequenceMem(1, self.neutype)
        
    def rememberANote(self,goalname,noteName,order):
        note = self.apac.encodingNote(noteName)
        if(order > len(self.msm.sequenceLayers.get(1).groups)):
            self.msm.sequenceLayers.get(1).addNewGroups(GroupID = order,layerID = 1,neunum = 128)
        tt = np.arange((order-1) * 5,order * 5,self.dt)
        for t in tt:
            self.ips.doRemebering(goalname, self.dt, t)            
            self.msm.doRemembering_note_only(note, order, self.dt, t)
        self.msm.doConnectToGoal(self.ips.goals.groups.get(goalname), order) 
        dic = {}
        if(configs.flag_experiments == False):
            
            dic["GoalSpike"] = self.ips.goals.groups.get(goalname).writeSpikeInfoToJson()
            dic["MSMSpike"] = self.msm.sequenceLayers.get(1).groups.get(order).writeSpikeInfoToJson()
           
            dic["Neuron"] = self.msm.sequenceLayers.get(1).groups.get(order).writeSelfInfoToJson("MSM")
            dic["GroupNum"] = order
        return dic
        
    def rememberANoteandTempo(self,goalname,composername,genrename, trackIndex,noteIndex,order,tinterval):
        instrumentTrack = self.msm.sequenceLayers.get(trackIndex)
        if(order > len(instrumentTrack.get("N").groups)):
            instrumentTrack.get("N").addNewGroups(GroupID = order,layerID = trackIndex,neunum = 129)
            instrumentTrack.get("T").addNewGroups(GroupID = order,layerID = trackIndex,neunum = 64)
        tt = np.arange((order-1) * 5,order * 5,self.dt)
        for t in tt:
            self.ips.doRemebering(goalname,self.dt, t)
            self.ips.doRememberingComposer(composername, self.dt, t) 
            self.ips.doRememberingGenre(genrename, self.dt, t)          
            self.msm.doRemembering(trackIndex,noteIndex, order, self.dt, t,tinterval)
        
        self.msm.doConnectToGoal(self.ips.goals.groups.get(goalname), instrumentTrack, order)
        self.msm.doConnectToComposer(self.ips.composers.groups.get(composername), instrumentTrack, order)
        self.msm.doConnectToGenre(self.ips.genres.groups.get(genrename), instrumentTrack, order)
        dic = {}
        ngraph = {}
        
        if(configs.RunTimeState == 0):
            dic["GoalSpike"] = self.ips.goals.groups.get(goalname).writeSpikeInfoToJson()
            dic["ComposerSpike"] = self.ips.composers.groups.get(composername).writeSpikeInfoToJson()
            dic["MSMSpike"] = instrumentTrack.get("N").groups.get(order).writeSpikeInfoToJson()
            dic["MSMTSpike"] = instrumentTrack.get("T").groups.get(order).writeSpikeInfoToJson()
                    
            temp = {} 
            temp[1] = instrumentTrack.get("N").groups.get(order).writeSelfInfoToJson("NMSM")
            temp[2] = instrumentTrack.get("T").groups.get(order).writeSelfInfoToJson("TMSM")
    #         dic["GroupNum"] = order
            
            Nodes = []
            Edges = []
            for key,td in temp.items():
                nlist = td.get("Neuron")
                for n in nlist:
                    #if(len(n.get('synapses')) > 0):
                    d = {}
                    d['id'] = n.get('area')+'_' + str(n.get('TrackID'))+'_' + str(n.get('GroupID'))+'_' + str(n.get('Index'))
                    d['area'] = n.get('area')
                    if(n.get('area') == 'NMSM'):
                        d['label'] = configs.notesMap.get(n.get('Index')-2)
                    else:
                        d['label'] = str(n.get('Index') * 60)
                    Nodes.append(d)
                    synlist = n.get('synapses')
                    for syn in synlist:
                        e = {}
                        #e['id'] = syn.get('Sarea') + '_'+str(syn.get('SgroupID'))+'_'+str(syn.get('Sindex')) + '_' +syn.get('Tarea') + '_'+str(syn.get('TgroupID')) + '_'+str(syn.get('Tindex'))
                        e['weight'] = str(syn.get('weight'))
                        e['source'] = syn.get('Sarea') + '_' +str(syn.get('StrackID'))+'_'+ str(syn.get('SgroupID'))+'_'+str(syn.get('Sindex'))
                        e['target'] = syn.get('Tarea') + '_' +str(syn.get('TtrackID')) + '_'+str(syn.get('TgroupID')) + '_'+str(syn.get('Tindex'))
                        
                        Edges.append(e)
        
            ngraph["node"] = Nodes
            ngraph["edge"] = Edges
        print(dic)              
        return dic,ngraph
        
    
    def actionSequenceMemoryInit(self):
        self.asm.createActionSequenceMem(1, self.neutype, 16)
       
    def recallMusicIPS(self,goalName):
        self.ips.setTestStates()
        self.msm.setTestStates()
        result = self.ips.doRecalling2(goalName, self.msm)
        return result
    
    def recallMusicByEpisode(self,episodeNotes): #using time window search episode
        self.ips.setTestStates()
        self.msm.setTestStates()
#         sl = self.msm.sequenceLayers.get(1)
#         for index,group in sl.groups.items():
#             strs = "group_"+str(index)+":"
#             for n in group.neurons:
#                 if(n.preActive == True):
#                     strs +=" neu_Index:"+str(n.index)+","
#             print(strs)
        result = self.msm.recallByEpisode2(episodeNotes,self.ips.goals)
        return result
    
    def generateEx_Nihilo(self,firstNote, durations, length):
        '''
        this function is used to generate the main melody, only one track
        '''
        self.ips.setTestStates()
        self.msm.setTestStates()
        result = {}
        track1 = []
        for i in range(length):
            dic = {}
            tt = np.arange(i * 5,(i+1) * 5,self.dt)
            for t in tt:
                self.ips.inhibiteGoals(self.dt, t)
                self.msm.generateEx_Nihilo(firstNote, durations, i, self.dt, t)
            
            panneu = []
            maxrate = 0.0
            maxneu = None
            for ni,neu in enumerate(self.msm.sequenceLayers.get(1).get("N").groups.get(i+1).neurons):
                if(neu.preActive == True):
                    panneu.append(neu)
                if(len(neu.spiketime) > 0):
                    #dic['N'] = neu.selectivity
                    if(len(neu.spiketime) > maxrate):
                        maxrate = len(neu.spiketime)
                        maxneu = neu
            print(maxneu.I)
            if(dic.get('N') == None):
                j = random.randint(0,len(panneu)-1)
                neu = panneu[j]
                neu.I = 20
                for t in tt:
                    neu.update_normal(self.dt,t)
                dic['N'] = neu.selectivity
            else: # chose the neuron which has the max firing rate
                dic['N'] = maxneu.selectivity
                    
                       
            patneu = []
            maxrate = 0.0
            maxneu = None
            for neu in self.msm.sequenceLayers.get(1).get("T").groups.get(i+1).neurons:
                if(neu.preActive == True):patneu.append(neu)
                if(len(neu.spiketime) > 0):
                    if(len(neu.spiketime) > maxrate):
                        maxrate = len(neu.spiketime)
                        maxneu = neu
            
            if(dic.get('T') == None):
                j = random.randint(0,len(patneu)-1)
                neu = patneu[j]
                neu.I = 20
                for t in tt:
                    neu.update_normal(self.dt,t)
                dic['T'] = neu.selectivity
            else:
                dic['T'] = neu.selectivity
            
            track1.append(dic)
        result[1] = track1
        print(result)
        return result
    
    
    def generateEx_Nihilo2(self,firstNote, durations, length):
        '''
        this function is used to generate the main melody, only one track
        '''
        self.ips.setTestStates()
        self.msm.setTestStates()
        result = {}
        track1 = []
        for i in range(length):
            dic = {}
            tt = np.arange(i * 5,(i+1) * 5,self.dt)
            for t in tt:
                self.ips.inhibiteGoals(self.dt, t)
                self.msm.generateEx_Nihilo(firstNote, durations, i, self.dt, t)
            
            panneu = []
            for ni,neu in enumerate(self.msm.sequenceLayers.get(1).get("N").groups.get(i+1).neurons):
                if(neu.preActive == True):
                    panneu.append(neu)
                if(len(neu.spiketime) > 0):
                    dic['N'] = neu.selectivity
                    
            if(dic.get('N') == None):
                j = random.randint(0,len(panneu)-1)
                neu = panneu[j]
                neu.I = 20
                for t in tt:
                    neu.update_normal(self.dt,t)
                dic['N'] = neu.selectivity
                    
                       
            patneu = []
            for neu in self.msm.sequenceLayers.get(1).get("T").groups.get(i+1).neurons:
                if(neu.preActive == True):patneu.append(neu)
                if(len(neu.spiketime) > 0):
                    dic['T'] = neu.selectivity
            
            if(dic.get('T') == None):
                j = random.randint(0,len(patneu)-1)
                neu = patneu[j]
                neu.I = 20
                for t in tt:
                    neu.update_normal(self.dt,t)
                dic['T'] = neu.selectivity
            
            track1.append(dic)
            result[1] = track1
        print(result)
        return result

    def generateEx_NihiloAccordingToGenre(self, genreName, firstNote, durations, length):
        self.ips.setTestStates()
        self.msm.setTestStates()
        result = {}
        track1 = []

        for i in range(length):
            dic = {}
            tt = np.arange(i * 5, (i + 1) * 5, self.dt)
            for t in tt:
                self.ips.inhibiteGoals(self.dt, t)
                self.ips.inhibitComposers(self.dt,t)
                self.ips.doRememberingGenre(genreName,self.dt,t)
                self.msm.generateEx_Nihilo(firstNote, durations, i, self.dt, t)

            panneu = []
            for ni, neu in enumerate(self.msm.sequenceLayers.get(1).get("N").groups.get(i + 1).neurons):
                if (neu.preActive == True):
                    panneu.append(neu)
                if (len(neu.spiketime) > 0):
                    dic['N'] = neu.selectivity

            if (dic.get('N') == None):
                j = random.randint(0, len(panneu) - 1)
                neu = panneu[j]
                neu.I = 20
                for t in tt:
                    neu.update_normal(self.dt, t)
                dic['N'] = neu.selectivity

            patneu = []
            for neu in self.msm.sequenceLayers.get(1).get("T").groups.get(i + 1).neurons:
                if (neu.preActive == True): patneu.append(neu)
                if (len(neu.spiketime) > 0):
                    dic['T'] = neu.selectivity

            if (dic.get('T') == None):
                j = random.randint(0, len(patneu) - 1)
                neu = patneu[j]
                neu.I = 20
                for t in tt:
                    neu.update_normal(self.dt, t)
                dic['T'] = neu.selectivity

            track1.append(dic)
            result[1] = track1
        print(result)
        return result

    def generateEx_NihiloAccordingToComposer(self, composerName, firstNote, durations, length):
        self.ips.setTestStates()
        self.msm.setTestStates()
        result = {}
        track1 = []

        for i in range(length):
            dic = {}
            tt = np.arange(i * 5, (i + 1) * 5, self.dt)
            for t in tt:
                self.ips.inhibiteGoals(self.dt, t)
                self.ips.doRememberingComposer(composerName, self.dt, t)
                self.msm.generateEx_Nihilo(firstNote, durations, i, self.dt, t)

    def recallActionIPS(self,goalName):
        self.ips.setTestStates()
        self.asm.setTestStates()
        self.ips.doRecalling(goalName, self.asm)
        
    def generate2TrackMusic(self,firstNotes, durations, lengths):
        self.ips.setTestStates()
        self.msm.setTestStates()
        result = {}
        for k,notes in firstNotes.items():
            track1 = []
            for i in range(lengths[k-1]):
                dic = {}
                tt = np.arange(i * 5,(i+1) * 5,self.dt)
                for t in tt:
                    self.ips.inhibiteGoals(self.dt, t)
                    #self.msm.generateSimgleTrackNotes(j+1, firstNotes[j], durations[j], i, self.dt, t)
                    self.msm.generateSimgleTrackNotes(k, notes, durations.get(k), i, self.dt, t)
                
                panneu = []
                for ni,neu in enumerate(self.msm.sequenceLayers.get(k).get("N").groups.get(i+1).neurons):
                    if(neu.preActive == True):
                        panneu.append(neu)
                    if(len(neu.spiketime) > 0):
                        dic['N'] = neu.selectivity
                        
                if(dic.get('N') == None):
                    j = random.randint(0,len(panneu)-1)
                    neu = panneu[j]
                    neu.I = 20
                    for t in tt:
                        neu.update_normal(self.dt,t)
                    dic['N'] = neu.selectivity
                        
                           
                patneu = []
                for neu in self.msm.sequenceLayers.get(k).get("T").groups.get(i+1).neurons:
                    if(neu.preActive == True):patneu.append(neu)
                    if(len(neu.spiketime) > 0):
                        dic['T'] = neu.selectivity
                
                if(dic.get('T') == None):
                    j = random.randint(0,len(patneu)-1)
                    neu = patneu[j]
                    neu.I = 20
                    for t in tt:
                        neu.update_normal(self.dt,t)
                    dic['T'] = neu.selectivity
                
                track1.append(dic)
            result[k] = track1
        print(result)
        return result
        
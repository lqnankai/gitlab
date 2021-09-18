'''
Created on 2016.7.6

@author: liangqian
'''
from midiprocess.readmidi import *
from midiprocess.play import *
from tools.msgq import *
from conf.conf import configs
from areas.cortex import Cortex
import pretty_midi
#import matplotlib.pyplot as plt
import json
import random
import math
from modal import pitch, synapse
import pygame
from mido import Message, MidiFile, MidiTrack
class EngineAPI():
    '''
    
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        self.cortex = Cortex(configs.neuron_type,configs.dt)
        self.conn = createMSQ()
        
    def cortexInit(self):
        #self.cortex.actionSequenceMemoryInit()
        self.cortex.musicSequenceMemroyInit()
    
    def rememberMusic(self,muiscName,composerName= "None"):
        muiscName = muiscName.title()
        composerName = composerName.title()
        self.cortex.ips.setTestStates()
        self.cortex.msm.setTestStates()
        self.cortex.addSubGoalToIPS(muiscName)
        self.cortex.addComposerToIPS(composerName)
        genreName = configs.GenreMap.get(composerName)
        self.cortex.addGenreToIPS(genreName)
        self.cortex.ips.innerLearning(muiscName,composerName,genreName)
        
        goaldic = {}
        composerdic = {}
        genredic = {}
        if(configs.RunTimeState == 0):
            g = self.cortex.ips.goals.groups.get(muiscName)
            c = self.cortex.ips.composers.groups.get(composerName)
            gre = self.cortex.ips.genres.groups.get(genreName)
            goaldic= g.writeSelfInfoToJson("IPS")
            composerdic = c.writeSelfInfoToJson("Composer")
            genredic = gre.writeSelfInfoToJson("Genre")
            graph = {}
            nodes = []
            edges = []
            nlist = goaldic.get("Neuron")
            for neu in nlist:
                n = {}
                n["id"] = neu.get("area") + "_"+str(neu.get("TrackID")) +"_"+str(neu.get("GroupID")) +"_"+str(neu.get("Index"))
                n["area"] = neu.get("area")
                n["label"] = goaldic.get("Name")
                nodes.append(n)
                synlist = neu.get('synapses')
                for syn in synlist:
                    e = {}
                    #e['id'] = syn.get('Sarea') + '_'+str(syn.get('SgroupID'))+'_'+str(syn.get('Sindex')) + '_' +syn.get('Tarea') + '_'+str(syn.get('TgroupID')) + '_'+str(syn.get('Tindex'))
                    e['weight'] = str(syn.get('weight'))
                    e['source'] = syn.get('Sarea') + '_' +str(syn.get('StrackID'))+'_'+ str(syn.get('SgroupID'))+'_'+str(syn.get('Sindex'))
                    e['target'] = syn.get('Tarea') + '_' +str(syn.get('TtrackID')) + '_'+str(syn.get('TgroupID')) + '_'+str(syn.get('Tindex'))
                     
                    edges.append(e)
            
            for neu in composerdic.get("Neuron"):
                n = {}
                n["id"] = neu.get("area") + "_"+str(neu.get("TrackID")) +"_"+str(neu.get("GroupID")) +"_"+str(neu.get("Index"))
                n["area"] = neu.get("area")
                n["label"] = composerdic.get("Name")
                nodes.append(n)
                synlist = neu.get('synapses')
                for syn in synlist:
                    e = {}
                    #e['id'] = syn.get('Sarea') + '_'+str(syn.get('SgroupID'))+'_'+str(syn.get('Sindex')) + '_' +syn.get('Tarea') + '_'+str(syn.get('TgroupID')) + '_'+str(syn.get('Tindex'))
                    e['weight'] = str(syn.get('weight'))
                    e['source'] = syn.get('Sarea') + '_' +str(syn.get('StrackID'))+'_'+ str(syn.get('SgroupID'))+'_'+str(syn.get('Sindex'))
                    e['target'] = syn.get('Tarea') + '_' +str(syn.get('TtrackID')) + '_'+str(syn.get('TgroupID')) + '_'+str(syn.get('Tindex'))
                      
                    edges.append(e)

            for neu in genredic.get("Neuron"):
                n = {}
                n["id"] = neu.get("area") + "_"+str(neu.get("TrackID")) +"_"+str(neu.get("GroupID")) +"_"+str(neu.get("Index"))
                n["area"] = neu.get("area")
                n["label"] = genredic.get("Name")
                nodes.append(n)
                
            graph["node"] = nodes
            graph["edge"] = edges
                
            jstr = json.dumps(graph)
            self.conn.send('/Queue/SampleQueue',jstr)
        return goaldic,composerdic
    
        
    
    def rememberMIDIMusic(self,musicName,composerName, fileName):
        musicName = musicName.title()
        composerName = composerName.title()
        print(musicName + " processing...")
        pm = pretty_midi.PrettyMIDI(fileName)
        genreName = configs.GenreMap.get(composerName)
        for i,ins in enumerate(pm.instruments):
            if(i >= 1): break;
            if(self.cortex.msm.sequenceLayers.get(i+1) == None):
                # create a new layer to store the track
                self.cortex.msm.createActionSequenceMem(i+1, self.cortex.neutype)
            self.rememberTrackNotes(musicName,composerName, genreName, i+1, ins, pm)
        print(musicName + " finished!")
                    
    
    def rememberTrackNotes(self,musicName,composerName,genreName,trackIndex,track,pm):
        r_notes = []
        r_intervals = []
        total_dic = {}
        
#         note_y_label = []
#         note_x = []
#         note_y = []
#         
#         tempo_y_label = []
#         tempo_x = []
#         tempo_y = []
        #rl = random.randint(10,40)
        print(track)
        rl = 5
        order = 1
        #for i,note in enumerate(track.notes):
        i = 0
        while(i < len(track.notes)):
            if(i >= rl):break;
            note = track.notes[i]
            start = pm.time_to_tick(note.start)
            end = pm.time_to_tick(note.end)
            pitches = []
            durations = []
            restFlag = False
            # this part recognizes a rest
            if(i == 0):# determine whether the first note is a rest
                if(start >= 30):
                    pitches.append(-1) #-1 represents a rest
                    durations.append(start/pm.resolution)
                    restFlag = True
            else:
                lastend = pm.time_to_tick(track.notes[i-1].end)
                if(start-lastend >=50):
                    pitches.append(-1)
                    durations.append((start-lastend)/pm.resolution)
                    restFlag = True
            if(restFlag == True):
                dic,g = self.rememberANote(musicName, composerName,genreName, trackIndex,pitches[0], order, durations[0], True)
                if(configs.RunTimeState == 0):
                    jstr = json.dumps(g)
                    self.conn.send('/Queue/SampleQueue',jstr)
                print(str(order)+":(-1,"+str(durations[0])+")")
                order = order + 1
                pitches = []
                durations = []    
            
            # this part recognizes a chord
            pitches.append(note.pitch)
            durations.append((end-start)/pm.resolution)
            j = i+1
            while(j < len(track.notes)):
                nextstart = pm.time_to_tick(track.notes[j].start)
                nextend = pm.time_to_tick(track.notes[j].end)
                #if(start == nextstart or end > nextstart):
                if(math.fabs(start-nextstart) <= 30 or end - nextstart >= 30):
                    pitches.append(track.notes[j].pitch)
                    durations.append((nextend-nextstart)/pm.resolution)
                    j = j+1
                else:
                    break
            i = j
#             str1 = str(order)+":("
#             for t in range(len(pitches)):
#                 str1 += str(pitches[t])+","+str(durations[t])+";"
#             print(str1+")") 
                    
            if(i < rl):
                dic,g = self.rememberANote(musicName, composerName, genreName, trackIndex, pitches[0], order, durations[0], True)
                str1 = str(order)+":("
                for t in range(len(pitches)):
                    str1 += str(pitches[t])+","+str(durations[t])+";"
                print(str1+")")
                order = order + 1
                if(configs.RunTimeState == 0):
                    jstr = json.dumps(g)
                    self.conn.send('/Queue/SampleQueue',jstr)
                    nlist = dic.get('MSMSpike')
                    ns = []
                    for l in nlist:
                        n = l.get('Index')
                        ns.append(n)
                    r_notes.append(ns)
                    tlist = dic.get('MSMTSpike')
                    ts = []
                    for l in tlist:
                        t = l.get('Index')
                        ts.append(t * 60)
                    r_intervals.append(ts)
            
    #                 for key, slist in dic.items():
    #                     if(key == "GoalSpike"):
    #                         for i,tdic in enumerate(slist[0].get("SpikeTime")):
    #                             note_y.append(128)
    #                             tempo_y.append(65*60)
    #                             note_y_label.append(musicName)
    #                             note_x.append(tdic.get(i+1))
    #                             tempo_x.append(tdic.get(i+1))
    #                     if(key == "MSMSpike"):
    #                         for i,tdic in enumerate(slist[0].get("SpikeTime")):
    #                             note_y.append(slist[0].get("Index"))
    #                             note_x.append(tdic.get(i+1))
    #                             note_y_label.append(configs.notesMap.get(slist[0].get("Index")))
    #                     if(key == "MSMTSpike"):
    #                         for i,tdic in enumerate(slist[0].get("SpikeTime")):
    #                             tempo_y.append(slist[0].get("Index")*60)
    #                             tempo_x.append(tdic.get(i+1))
    #                             #tempo_y_label.append(tdic.get(i+1) * 60)
#         # add to total_dic
#         fig = plt.figure()
#         ax1 = fig.add_subplot(1,1,1)
#         #ax2 = fig.add_subplot(1,2,2)
#         ax1.set_title("Spatial Subnetwork of Track1")
#         ax1.scatter(note_x,note_y,c = "k",marker="|")
#         plt.yticks(note_y,note_y_label)
# #         ax2.set_title("Temporal Subnetwork of Track1")
# #         ax2.scatter(tempo_x,tempo_y,c="r",marker="|")
#         plt.show()
        #write midi file
        #play_notes('result_'+musicName, r_notes, r_intervals,standardClock)
        #jstr = json.dumps(total_dic)
        return total_dic
            
    def rememberNotes(self,MusicName,notes,intervals,tempo = True):
        jStr = ''
        #print(intervals)
        notesStr = notes.split(",")
        intervalsStr = intervals.split(",")
        intervaltimes = []
        for i in range(len(intervalsStr)-1):
            intervaltimes.append(int(intervalsStr[i]))
        print(intervaltimes)
        for i,note in enumerate(notesStr):
            note = int(note)
            if(i < len(notesStr)-1):
                tinterval = intervalsStr[i]
                tinterval = int(intervalsStr[i])
            self.rememberANote(MusicName, note, i+1, tinterval, tempo)
        return jStr
        
    
    def rememberANote(self,MusicName,ComposerName, genreName, TrackIndex,NoteIndex,order,tinterval,tempo = False):
        if(tempo == False):
            dic = self.cortex.rememberANote(MusicName, NoteIndex, order)
            jsonStr = json.dumps(dic)
            return jsonStr
        else:
            dic,g = self.cortex.rememberANoteandTempo(MusicName,ComposerName,genreName, TrackIndex,NoteIndex, order,tinterval)
            return dic,g
        
    def recallMusic(self,musicName):
        result = self.cortex.recallMusicIPS(musicName)
        print(result)
        noteResult = {}
#         for tindex,track in result.items():
#             tmp = {}
#             n = configs.notesMap.get(value)
#             tmp["id"] = value
#             tmp["name"] = n
#             noteResult[key] = tmp
#             
#         jsonStr = json.dumps(noteResult)
#         print(jsonStr)
        return noteResult
    
    def recallEpisode(self,episodeNotes):
        result = self.cortex.recallMusicByEpisode(episodeNotes)
        dic = {}
        epinotes = {}
        for i,en in enumerate(episodeNotes):
            tmp = {}
            tmp["id"] = en
            n = configs.notesMap.get(en)
            tmp["name"] = n
            epinotes[i+1] = tmp
        goalMap = {}
        for i,res in enumerate(result):
            if(goalMap.get(res.get('goal')) !=None):continue
            goalMap[res.get('goal')] = 1
            restnotes = {} 
            resdic = {}
            rest = res.get('rest')
            count = 1
            for tdic in rest.values():
                tmp = {}
                fre = tdic.get("N")
                tmp["id"] = fre
                n = configs.notesMap.get(fre)
                tmp["name"] = n
                tmp["duration"] = tdic.get("T")
                restnotes[count] = tmp
                count += 1
            resdic['episodenotes'] = epinotes
            resdic['rest'] = restnotes
            resdic['goal'] = res.get('goal')
            dic[i] = resdic
        #jsonStr = json.dumps(dic)
        print(dic)
        return dic
            
    def generateEx_Nihilo(self, firstNote, durations,length):
        '''
        parameters:
        fistNote: Specify the beginning notes to generate a note
        length: the length of the generated music
        '''
        result = self.cortex.generateEx_Nihilo2(firstNote, durations, length)
        return result

    def generateEx_NihiloAccordingToGenre(self, genreName, firstNote, durations, length):

         result = self.cortex.generateEx_NihiloAccordingToGenre(genreName, firstNote, durations, length)

    def generateEx_NihiloAccordingToComposer(self, composerName, firstNote, durations, length):

        result = self.cortex.generateEx_NihiloAccordingToComposer(composerName, firstNote, durations, length)
        return result

    def generate2TrackMusic(self,firstNotes,durations, lengths):
        result = self.cortex.generate2TrackMusic(firstNotes, durations, lengths)   
        return result 
    
    def test(self):
        sl = self.cortex.msm.sequenceLayers.get(1)
        for index, group in sl.groups.items():
            strs = "group_"+str(index)+":"
            for n in group.neurons:
                if(n.preActive == True):
                    strs +=" neu_Index:"+str(n.index)+","
            print(strs)
            
    def saveModetoFile(self,fname):
        '''
            1. Save all neurons in a file
            2. Save all synapses in a file
        '''   
        basic_f = open(fname + "_basic.csv","w")
        neu_f = open(fname + "_neuron.csv",'w')
        link_f = open(fname + "_synapse.csv",'w')
        # save basic information of neurons first
        strs = "IPS," + str(len(self.cortex.ips.goals.groups)) + "\n"
        basic_f.write(strs)
        strs = "trackNum," + str(len(self.cortex.msm.sequenceLayers))+"\n"
        basic_f.write(strs)
        
        for key, tracks in self.cortex.msm.sequenceLayers.items():
            strs = "track," + str(key) + "," + str(len(tracks.get("N").groups)) + "\n"
            basic_f.write(strs)
            
#         for g in self.cortex.ips.goals.groups.values():
#             for n in g.neurons:
#                 nID = "0," + n.areaName + "," + str(n.groupIndex) + "," + str(n.index) + "," + str(g.name)+ "," + str(int(n.preActive)) + "\n"
#                 neu_f.write(nID)
#                 for syn in n.synapses:
#                     if(syn.weight == 0): continue
#                     strs = ""
#                     strs1 = str(syn.pre.layerIndex) + "_" + syn.pre.areaName[0] + "_" + str(syn.pre.groupIndex) + "_" + str(syn.pre.index) +","
#                     strs2 = str(syn.post.layerIndex) + "_" + syn.post.areaName[0] + "_" + str(syn.post.groupIndex) + "_" + str(syn.post.index) +"," + str(syn.weight) + ","+str(syn.delay)+","+str(syn.type)
#                     strs = strs1 + strs2 + "\n"
#                     link_f.write(strs)
                
        for tl in self.cortex.msm.sequenceLayers.values():
            for sl in tl.values():
                for g in sl.groups.values():
                    for n in g.neurons:
                        nID = str(n.layerIndex) +"," + n.areaName[0] +"," + str(n.groupIndex) + "," + str(n.index) + "," + str(n.selectivity)+ "," + str(int(n.preActive)) + "\n"
                        neu_f.write(nID)
                        
                        for syn in n.synapses:
                            if(syn.weight == 0): continue
                            strs = ""
                            strs1 = str(syn.pre.layerIndex) + "_" + syn.pre.areaName[0] + "_" + str(syn.pre.groupIndex) + "_" + str(syn.pre.index) +","
                            strs2 = str(syn.post.layerIndex) + "_" + syn.post.areaName[0] + "_" + str(syn.post.groupIndex) + "_" + str(syn.post.index) +"," + str(syn.weight) + ","+str(syn.delay)+","+str(syn.type)
                            strs = strs1 + strs2 + "\n"
                            link_f.write(strs)                  
        basic_f.close()
        neu_f.close()
        link_f.close()
        
    def loadModel(self, basicFile, neuronFile, synFile):
        print("loading the model.........")
        basic_f = open(basicFile,'r')
        neu_f = open(neuronFile,'r')
        link_f = open(synFile,'r')
        lines = basic_f.readlines()
        goalsNum = 0
        trackNum = 0
        tracklen = {}
        for line in lines:
            line = line.strip()
            strs = line.split(",")
            if(strs[0] == "IPS"):
                goalsNum = int(strs[1])
            if(strs[0] == "trackNum"):
                trackNum = int(strs[1])
            if(strs[0] == "track"):
                tracklen[int(strs[1])] = int(strs[2])
                
        #create model
        gdic = {}
#         for i in range(goalsNum):
#             self.cortex.ips.addNewSubGoal("")
        for i in range(trackNum):
            self.cortex.msm.createActionSequenceMem(i+1, 'LIF')
        for key, len in tracklen.items():
            instrumentTrack = self.cortex.msm.sequenceLayers.get(key)
            nl = instrumentTrack.get("N")
            tl = instrumentTrack.get("T")
            for i in range(len):
                nl.addNewGroups(i+1, key, 129)
                tl.addNewGroups(i+1, key ,64)
        
        # add attributes
        nline = neu_f.readline()
        while(nline):
            nline = nline.strip()
            strs = nline.split(",")
            tid = int(strs[0])
            gid = int(strs[2])
            nid = int(strs[3])
            sel = strs[4]
            flag = int(strs[5])
            if(strs[1] != "IPS"):
                n = self.cortex.msm.sequenceLayers.get(tid).get(strs[1]).groups.get(gid).neurons[nid-1]
                #print("a")
                n.selectivity = float(sel)
                if(flag == 1):n.preActive = True
                else: n.preActive = False
            else:
                gdic[gid] = sel
                self.cortex.ips.addNewSubGoal(sel)
                n = self.cortex.ips.goals.groups.get(sel).neurons[nid-1]
                n.selectivity = sel
                n.preActive = flag
            nline = neu_f.readline()
                
        sline = link_f.readline()
        while(sline):
            sline = sline.strip()      
            strs = sline.split(",")
            weight = float(strs[2])
            delay = int(strs[3])
            stype = int(strs[4])
            pres = strs[0].split("_")
            posts = strs[1].split("_")
            pre = None
            post = None
            if(pres[1] == "I"):
                gid = gdic.get(int(pres[2]))
                pre = self.cortex.ips.goals.groups.get(gid).neurons[int(pres[3])-1]
            else:
                pre = self.cortex.msm.sequenceLayers.get(int(pres[0])).get(pres[1]).groups.get(int(pres[2])).neurons[int(pres[3])-1]
                
            if(posts[1] == "I"):
                gid = gdic.get(int(posts[2]))
                post = self.cortex.ips.goals.groups.get(gid).neurons[int(posts[3])-1]
            else:
                post = self.cortex.msm.sequenceLayers.get(int(posts[0])).get(posts[1]).groups.get(int(posts[2])).neurons[int(posts[3])-1]
            syn = synapse.Synapse(pre,post)
            syn.weight = weight
            syn.delay = delay
            syn.type = stype
            post.synapses.append(syn)
            sline = link_f.readline()
            
            
        basic_f.close()
        neu_f.close()
        link_f.close()
        print("model is loaded!")
        
    def writeMIDIfile(self, fileName, midic):
        '''
        midic format description
        midic = {1:
                {1:{'N':71}}
        }
        '''
        
        fileName += "+exnih.mid"
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        track.append(Message('program_change', program = 1,time = 0))
        for tks in midic.values():
            for dic in tks:
                id = int(dic.get('N'))
                if(id == -1):continue
                dur = int(dic.get('T') * 480)
                track.append(Message('note_on', note= id, velocity=64, time=0))
                track.append(Message('note_off', note= id, velocity=64, time=dur))
        
        mid.save(fileName)
        
    def writeMIDIfile2(self, fileName,midic):
        '''
        midic format description:
        midic = {1:[{'N':71,'T':0.5}.....],
                 2:[{'N':60,'T':0.25}.....],
                 ....
        }
        '''
        
        if(len(midic) == 1):
            fileName += "+exnih.mid"
        else:
            fileName += "+multi_track.mid"
        mid = MidiFile()
        
        for tks in midic.values():
            print(tks)
            track = MidiTrack()
            mid.tracks.append(track)
            track.append(Message('program_change', program = 1,time = 0))
            for dic in tks:
                id = int(dic.get('N'))
                #######
                if(id == -1):continue
                dur = int(dic.get('T') * 480)
                track.append(Message('note_on', note= id, velocity=64, time=0))
                track.append(Message('note_off', note= id, velocity=64, time=dur))
        
        mid.save(fileName)
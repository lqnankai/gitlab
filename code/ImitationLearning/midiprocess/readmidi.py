'''
Created on 2018.8.3

@author: liangqian
'''

from midiprocess.midiparser import MidiParser
from modal.note import Note
from modal.pitch import Pitch
import string

def midiFileParser(filename):
    f = open(filename,"rb")
    par = MidiParser(f)
    smf = par.read_all()
    fns = filename.split("/")
    ss = fns[len(fns)-1]
    ind = ss.index(".")
    f = open(ss[0:ind]+".txt","w")
    f.write(smf.__str__())
    f.close()
    track_notes = {}
    count = 1
    for m in range(1,len(smf.tracks)):
        nevents = smf.tracks[m].events
        notes = []
    
        i = 0
        while(i < len(nevents)):
            if(nevents[i].status == 144 and nevents[i].data[1] > 0):
                j = i+1
                while(j < len(nevents)):
                    if((nevents[j].status == 128 or nevents[j].data[1] == 0) and nevents[j].data[0] == nevents[i].data[0]):
                        break
                    else:
                        j = j+1
                t = j-i
                n = Note()
                if(t == 1): #common situation
                    p = Pitch()
                    p.frequence = nevents[j].data[0]
                    n.pitches.append(p)
                    n.lastTime.append(nevents[j].delta_time)
                    notes.append(n)
                    i = j+1
                else: # judging chord 
                    on_index = []
                    off_index = []
                    flag = True
#                     on_index.append(i)
#                     off_index.append(j)
                    for u in range(i+1,j):
                        #print(nevents[u])
                        if(nevents[u].status == 144 and nevents[u].data[1] >0):
                            on_index.append(u)
                        else:break # not continuous 144 events
                    if(len(on_index) == 0): flag = False
                    else:
                        num_pitches_chord = len(on_index)+1
                        for on in on_index:
#                             print(nevents[on])
                            #for s in range(u, u+num_pitches_chord+1):
                            for s in range(u,j):
#                                 print(nevents[s])
                                if((nevents[s].status == 128 or nevents[s].data[1] == 0) and nevents[on].data[0] == nevents[s].data[0]):
                                    off_index.append(s)
                                    break
                        if(len(on_index) != len(off_index)):flag = False
                        else: flag = True
                    
                    if(flag == False):
                        p = Pitch()
                        p.frequence = nevents[j].data[0]
                        n.pitches.append(p)
                        duration = 0
                        for s in range(i+1,j+1):
                            duration += nevents[s].delta_time
                        n.lastTime.append(duration)
                        notes.append(n)
                        i = i+1
                    else:
                        chord_duration = nevents[j].delta_time
                        for off in off_index:
                            chord_duration += nevents[off].delta_time
                        for on in on_index:
                            chord_duration += nevents[on].delta_time
                        p = Pitch()
                        p.frequence = nevents[i].data[0]
                        n.pitches.append(p)
                        n.lastTime.append(chord_duration)
                        for on in on_index:
                            p = Pitch()
                            p.frequence = nevents[on].data[0]
                            n.pitches.append(p)
                            n.lastTime.append(chord_duration)
                        notes.append(n)
                        
                        i = j+1
                                
            else:
                i = i+1
        if(len(notes) >0):
            track_notes[count] = notes
            count += 1 
    return smf,track_notes
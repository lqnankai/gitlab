'''
Created on 2020.08.03

@author: liangqian
'''
import pretty_midi
from mido import Message, MidiFile, MidiTrack

fileName2 = "../midifiles/prelude C major.mid"
pm = pretty_midi.PrettyMIDI(fileName2)
# f = open("roll.csv","w")
# aa = pm.get_piano_roll(100)
# for i in range(128):
#     f.write(str(i)+",")
# f.write("\n")
# for i in range(pm.get_piano_roll(100).shape[1]):
#     a = aa[:,i]
#     for j in range(len(a)):
#         f.write(str(a[j])+",")
#     f.write("\n")
# 
# f.close()
    #print(aa[:,i])
f = open("memory.csv","w")
f.write("area,index,starttime,endtime\n")
# f.write("Hippocampus-genre,1,0,end,\n")
# f.write("Hippocampus-composer,2,0,end,\n")
f.write("cHipp,1,0,end,\n")
count = 0
for i,track in enumerate(pm.instruments):
    for j,note in enumerate(track.notes):
        index = count
        p = note.pitch
        s = note.start
        e = note.end
        f.write("A41/42,"+str(count)+","+str(s)+","+str(e)+",\n")
        count += 1
f.close()
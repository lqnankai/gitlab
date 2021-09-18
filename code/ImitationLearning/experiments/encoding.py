'''
Created on 2019.4.2

@author: liangqian
'''
import numpy as np
import math
from midiprocess.readmidi import *
from numpy import real

ulist = np.arange(60,3900,60)
sigma = 23

tmp = ((91-60)*(91-60))/(2*sigma*sigma)
p = (1/(math.sqrt(2*math.pi) * sigma))* math.exp(-tmp)
p = p*1000
print(p)
# 
# testSet = np.random.randint(0,3900,1000)

musicName = "Sonate C major"
#fileName = "../midifiles//classic midi/chopin/chpn-p15.mid"
fileName = "../midifiles/classic midi/mozart/mz_545_1.mid"
    
# for i,s in enumerate(testSet):
#     index = s/60
#     for j,u in enumerate(ulist):
#         tmp = ((s-u)/sigma)**2
#         p = (1/(math.sqrt(2*math.pi) * sigma)) * math.exp(tmp)


# testSet = np.random.randint(90,150,100)
# print(testSet)

smf,track_notes = midiFileParser(fileName)
durDic = {}
cunt = 0
for i,notes in track_notes.items():
    cunt += len(notes)
    for j,note in enumerate(notes):
        if(j == 145):
            print("debug")
        #print(str(j) + ":"+ str(notes[j].pitches[0].frequence) + ":"+str(notes[j].lastTime))
        t = note.lastTime[0]
#         for r,d in enumerate(ulist):
#             if(t <= d+30 and t >= d-30):
#                 if(durDic.get(d) == None):
#                     durDic[d] = 1
#                     break
#                 else:
#                     tmp = durDic.get(d)
#                     durDic[d] = tmp+1
#                     break
        flag = False
        for r,d in enumerate(ulist):
            tmp = ((t-d)*(t-d))/(2*sigma*sigma)
            p = (1/(math.sqrt(2*math.pi) * sigma))* math.exp(-tmp)
            p = p*1000
            if(p >= 7.4):
                if(durDic.get(d) == None):
                    durDic[d] = 1
                else:
                    tmp = durDic.get(d)
                    durDic[d] = tmp+1
                flag = True
                break
        if(flag == False):
            print(i)
            print(j)
            print(note.pitches[0].frequence)
            print(note.lastTime)
print(cunt)
print(durDic)
realdic = {}
rf = open("./mozart.txt","r")
line = rf.readline()


while(len(line) > 0):
    strs = (line.strip()).split(":")
    realdic[int(strs[0])] = int(strs[1]) 
    line = rf.readline()
rf.close()
print(realdic)

durDic = {60:144,120:1707,240:200,480:248,720:20,960:14,1920:1}

  
        
        
        
        
        
        
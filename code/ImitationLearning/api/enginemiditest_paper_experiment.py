'''
Created on 2019.4.2

@author: liangqian
'''
#from api.engineapi import EngineAPI
from conf.conf import *
from GUI.globaldata import brainEngine
from midiprocess.readmidi import *
import matplotlib.pyplot as plt
import random
import numpy as np
import os

# musicName = "prelude C major"
# fileName = "../midifiles/prelude C major.mid"

# musicName = "#C minor moonlight"
# fileName = "../midifiles/#C minor moonlight.midi"

musicName = "Nocturne in b flat minor"
fileName = "../midifiles/Nocturne in b flat minor.midi"







#----------------------------------------Learning experiments-------------------------------------------      
# path = "../midifiles/classic midi"
# y = []
# x_label = []
# x=[]
# y_increase = []
# count = 0
# lastmax = 0
# for dir in os.listdir(path):
#     dpath = os.path.join(path,dir)
#     if os.path.isdir(dpath):
#         for f in os.listdir(dpath):
#             count += 1
#             fname = (os.path.join(dpath,f))
#             smf,track_notes = midiFileParser(fname)
#             num = 0
#             for key,notes in track_notes.items():
#                 num += len(notes)
#             if(num > lastmax):
#                 lastmax = num
#             y_increase.append(lastmax*2+count)
#             x.append(count)
#             strs = f.split(".")
#             x_label.append(strs[0])
#             y.append(num)
#  
# print(lastmax)          
# fig = plt.figure()
# ax1 = fig.add_subplot(1,2,1)
# ax1.set_title("Note Number Of Musical Works")
# ax1.bar(x,y,color="b")
# ax1.set_xticks(range(0,331,50))
# ax1.set_xticklabels(x_label[::50],rotation=20)
# ax1.set_xlabel("Musical Works")
# ax1.set_ylabel("Number of Notes")
# # plt.xticks(x, x_label)
#  
# ax2 = fig.add_subplot(1,2,2)
# ax2.set_title("Increasing Curve Of Network")
# ax2.plot(x,y_increase)
# ax2.set_xticks(range(0,331,50))
# ax2.set_xticklabels(x_label[::50],rotation=20)
# ax2.set_xlabel("Musical Works")
# ax2.set_ylabel("Number of Neurons")
#  
# plt.show()
# ----------------------------------------------- end -----------------------------------------------------

#------------------------------------------------Retrieving experiments-------------------------------------
#**********************goal retrieving********************#
path = "..\midifiles\classic midi"
num_count = 5
filePathList = []
namelist = []
for dir in os.listdir(path):
    dpath = os.path.join(path,dir)
    if os.path.isdir(dpath):
        for f in os.listdir(dpath):
            fname = (os.path.join(dpath,f))
            filePathList.append(fname)
            namelist.append(f)
            #smf,track_notes = midiFileParser(fname)
 
f = open("goal_result.csv","a+")             
rl = random.sample(range(0,330),num_count)
for index in rl:
    fileName = filePathList[index]
    musicName = namelist[index]
    brainEngine.rememberMusic(musicName)
    notes,totaldic = brainEngine.rememberMIDIMusic(musicName, fileName)
    result = brainEngine.recallMusic(musicName)
    count = 0
    for key,td in result.items():
        if(td.get("id") == notes[key-1].pitches[0].frequence):
            count += 1
    strs = musicName +","+str(len(result))+","+str(count)+","+str(float(count)/float(len(result)))+"\n"
    f.write(strs)
f.close()    
           
x_label= []
x = []
y = []
 
f = open("goal_result.csv","r")
line = f.readline()
count = 1
while(len(line) > 0):
    strs = (line.strip()).split(",")
    x.append(count)
    x_label.append(strs[0])
    y.append(strs[1])
    line = f.readline()
    count += 1
 
fig = plt.figure()
 
ax1 = fig.add_subplot(1,1,1)
ax1.set_title("Goal-Retrieving Accuracy")
ax1.plot(x,y,color="b")
ax1.set_xticks(range(0,50,5))
ax1.set_xticklabels(x_label[::5],rotation=20)
ax1.set_xlabel("Musical Works")
ax1.set_ylabel("Retrieving Accuracy")
 
plt.show()

#**********************Episodic retrieving********************#          
# smf,track_notes = midiFileParser("../midifiles/Nocturne in b flat minor.midi")
# path = "../midifiles/temptrainning" 
# # num_count = 1
# # filePathList = []
# # namelist = []
# for dir in os.listdir(path):
#     dpath = os.path.join(path,dir)
#     brainEngine.rememberMusic(dir)
#     brainEngine.rememberMIDINotes(dir, dpath)
# #brainEngine.test()
#     
# 
# testpath = "../midifiles/testEpisode"
# for dir in os.listdir(testpath):
#     dpath = os.path.join(testpath,dir)
#     if os.path.isdir(dpath):
#         for f in os.listdir(dpath):
#             fname = (os.path.join(dpath,f))
#             smf,track_notes = midiFileParser(fname)
#             episodeNotes = []
#             for n in track_notes.get(1):
#                 episodeNotes.append(n.pitches[0].frequence)
#             
#             #begine recall
#             dic = brainEngine.recallEpisode(episodeNotes)
# #             if(len(dic) >0):
# #                 rf = open("result_"+f+".csv","w")
# #                 for k, res in dic.items():
# #                     rf.write(res.get("goal")+"\n")
# #                     strs1 = "episode,"
# #                     ens = res.get("episodenotes")
# #                     for k1, en in ens.items():
# #                         strs1 += en.get("id")+","
# #                     strs1 += "\n"
# #                     rf.write(strs1)
# #                     strs2 = "rest,"
# #                     rns = res.get("rest")
# #                     for k1, rn in rns.items():
# #                         strs2 += rn.get("id")+","
# #                     strs2 += "\n"
# #                     rf.write(strs2)
# #                 rf.close()

#*******************paper--clock neuron---a trick***************#
# musicName = "Sonate C major"
# fileName = "../midifiles/prelude C major.mid"
# 
# smf,track_notes = midiFileParser("../midifiles/Sonate C major.mid")
# 
# 
# x = np.arange(0,400)
# cy1= np.zeros(len(x))
# cy2= np.zeros(len(x))
# for i in range(0,len(x),1):
#     cy1[i]=100
# for i in range(0,len(x),3):
#     cy2[i]=100   
# fig = plt.figure()
# 
# notes = track_notes[1]
# ny1 = np.zeros(len(x))
# ny2 = np.zeros(len(x))
# t_end = 0
# for i in range(7):
#     print(i)
#     p = notes[i].pitches[0].frequence
#     t_ori = int(notes[i].lastTime[0]/14)
#     for j in range(t_end,t_end+t_ori,2):
#         ny1[j]=p
#     t_end += t_ori     
# t_end = 0       
# for i in range(7):
#     print(i)
#     p = notes[i].pitches[0].frequence
#     t_ori = int(notes[i].lastTime[0]/10)
#     for j in range(t_end,t_end+t_ori,2):
#         ny2[j]=p
#     t_end += t_ori   
#     
#     
#     
# y_ticklabels = []
# nmap = configs.notesMap
# for i in range(60,99):
#     #str = nmap.get(i)
#     y_ticklabels.append(str(i))
# y_ticklabels.append('clock')
#        
# 
# ax1 = fig.add_subplot(2,1,1)
# #ax1.set_title("f=8.8")
# ax1.scatter(x,cy1,marker='|',color="b")
# #ax1.scatter(x,cy2,marker='|',color="r")
# ax1.scatter(x,ny1,marker='|',color='b')
# ax1.set_xticks(range(0,400,20))
# ax1.set_ylim(60,101)
# #ax1.set_yticklabels(y_ticklabels)
# #ax1.set_yticks(range(60,80,2))
# #ax1.set_xticklabels(x_label[::100])
# ax1.set_xlabel("time")
# ax1.set_ylabel("neuron index")
# 
# ax2 = fig.add_subplot(2,1,2)
# #ax2.set_title("f=8.8")
# #ax2.scatter(x,cy1,marker='|',color="b")
# ax2.scatter(x,cy2,marker='|',color="r")
# ax2.scatter(x,ny2,marker='|',color='r')
# ax2.set_xticks(range(0,400,20))
# ax2.set_ylim(60,101)
# #ax1.set_yticklabels(y_ticklabels)
# #ax1.set_yticks(range(60,80,2))
# #ax1.set_xticklabels(x_label[::100])
# ax2.set_xlabel("time")
# ax2.set_ylabel("neuron index")
#  
# plt.show()        
        
        

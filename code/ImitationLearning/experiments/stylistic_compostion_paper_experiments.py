'''
Created on 2021.0.20

@author: liangqian
'''


from conf.conf import *
from GUI.globaldata import brainEngine
from midiprocess.readmidi import *
from modal.izhikevichneuron import IzhikevichNeuron
import matplotlib.pyplot as plt
import random
import numpy as np
import os
import pretty_midi
# import seaborn as sns
# import pandas as pd

from mido import Message, MidiFile, MidiTrack


#------------------------------------------------encoding---------------------------------------------#
# neu = IzhikevichNeuron(a = 0.01,b=0.2,c=-65,d=8)
# dt = 0.1
# T = 1000
# step = int(T/dt)
# time = np.arange(0,T,dt)
# spikes = np.zeros(step)
# for i in range(0,step):
#     neu.update(dt,time[i])
# print(len(neu.spiketime))
# for s in neu.spiketime:
#     t = int(s*10)
#     spikes[t] = 1 
# 
# 
# fileName1 = "../midifiles/Sonate C major.mid"
# pm = pretty_midi.PrettyMIDI(fileName1)
# notes = pm.instruments[0].notes
# print(pm.instruments[0].notes[0].pitch)
# time = np.arange(0,10000,dt)
# pitchspikes = np.zeros(100000)
# 
# x1 = []
# y1 = []
# 
# for i in range(0,10):
#     p = notes[i].pitch
#     for s in neu.spiketime:
#         temp = int(s*10)+random.randint(0,1000)+i*10000
#         x1.append(temp)
#         y1.append(p)
# for i in range(0,10):
#     for s in neu.spiketime:
#         temp = int(s*10)+random.randint(0,1000)+i*10000
#         x1.append(temp)
#         y1.append(128)
# for i in range(0,10):
#     for s in neu.spiketime:
#         temp = int(s*10)+random.randint(0,1000)+i*10000        
#         x1.append(temp)
#         y1.append(130)
# for i in range(0,10):
#     for s in neu.spiketime:
#         temp = int(s*10)+random.randint(0,1000)+i*10000
#         x1.append(temp)
#         y1.append(132)
# 
# 
# y_label = []
# for key,value in configs.notesMap.items():
#     if(key <70):continue
#     y_label.append(str(value))
# y_label.append("Sonate C major")
# y_label.append("Mozart")
# y_label.append("Classical")
# 
# 
#     
# x2 = []
# y2 = []
# res = pm.resolution
# for i in range(0,10):
#     start = pm.time_to_tick(notes[i].start)
#     end = pm.time_to_tick(notes[i].end)
#     d = end-start
#     for s in neu.spiketime:
#         temp = int(s*10)+random.randint(0,1000)+i*10000
#         x2.append(temp)
#         y2.append(d)
# for i in range(0,10):
#     for s in neu.spiketime:
#         temp = int(s*10)+random.randint(0,1000)+i*10000
#         x2.append(temp)
#         y2.append(1500)
# for i in range(0,10):
#     for s in neu.spiketime:
#         temp = int(s*10)+random.randint(0,1000)+i*10000        
#         x2.append(temp)
#         y2.append(1550)
# for i in range(0,10):
#     for s in neu.spiketime:
#         temp = int(s*10)+random.randint(0,1000)+i*10000
#         x2.append(temp)
#         y2.append(1600)
# 
# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)      
# ax1.scatter(x1,y1,marker='|',color="red")
# # ax1.set_ylim(60,140)
# #ax1.set_yticks(range(70,150,5))
# #ax1.set_yticklabels(y_label)
# 
# # ax2 = fig.add_subplot(1,1,1)
# # ax2.scatter(x2,y2,marker='|',color="black")
# 
# plt.show()
    
    
#-----------------------------------------------------oscillation waves-------------------------------------------------#
#------------Theta waves--------------#
# fileName1 = "../midifiles/Sonate C major.mid"
# pm = pretty_midi.PrettyMIDI(fileName1)
# dt = 0.1
# step = int(1000/dt)
# time1 = np.arange(0,1000,dt)
# name1 = ["Classical","Mozart","Sonate C major","72(C5)","others"]
# neus1 = {}
# Iext1 = [5,5,5,4.2,0]
# for i in range(5):
#     n = IzhikevichNeuron(a = 0.01,b=0.2,c=-65,d=8)
#     spikes = np.zeros(step)
#     n.I_ext = Iext1[i]
#     for j in range(0,step):
#         n.update(dt,time1[j])
#         spikes[j] = n.v
#     neus1[i] = spikes
#  
# neus2 = {}
# Iext2 = [5,5,5,4.8,0]
# name2 = ["Classical","Mozart","Sonate C major","76(E5)","others"]
# time2 = np.arange(1000,2000,dt)
# for i in range(5):
#     n = IzhikevichNeuron(a = 0.01,b=0.2,c=-65,d=8)
#     spikes = np.zeros(step)
#     n.I_ext = Iext2[i]
#     for j,t in enumerate(time2):
#         n.update(dt,t)
#         spikes[j] = n.v
#     neus2[i] = spikes
#  
#  
# neus3 = {}
# Iext3 = [5,5,5,5.4,0]
# time3 = np.arange(2000,3000,dt)
# name3 = ["Classical","Mozart","Sonate C major","79(G5)","others"]
# for i in range(5):
#     n = IzhikevichNeuron(a = 0.01,b=0.2,c=-65,d=8)
#     spikes = np.zeros(step)
#     n.I_ext = Iext3[i]
#     for j,t in enumerate(time3):
#         n.update(dt,t)
#         spikes[j] = n.v
#     neus3[i] = spikes
#  
# plt.figure()
# for i in range(0,5):
#     titles = "neuron:"+ name1[i]
#     plt.subplot(3,5,i+1)
#     plt.title(titles)
#     plt.plot(time1,neus1.get(i),color="orange")
#  
# for i in range(0,5):
#      
#     plt.subplot(3,5,i+1+5)
#     plt.title("neuron:"+ name2[i])
#      
#     plt.plot(time2,neus2.get(i),color="tomato")
#  
# for i in range(0,5):
#     plt.subplot(3,5,i+1+10)
#     plt.title("neuron:"+ name3[i])
#     plt.plot(time3,neus3.get(i),color="seagreen")  
# plt.show()


#------------gamma waves--------------#
dt = 0.1
step = int(1000/dt)
time1 = np.arange(0,1000,dt)
name1 = ["Classical","A5","interneurons"]
neus1 = {}
Iext1 = [30,30,5]
for i in range(3):
    if(i < 2):
        n = IzhikevichNeuron(a = 0.01,b=0.2,c=-65,d=8)
        spikes = np.zeros(step)
        n.I_ext = Iext1[i]
        for j in range(0,step):
            n.update(dt,time1[j])
            spikes[j] = n.v
        neus1[i] = spikes
    else:
        n = IzhikevichNeuron(a=0.1,b=0.2,c=-65,d=2)
        spikes = np.zeros(step)
        n.I_ext = Iext1[i]
        for j in range(0,step):
            n.update(dt,time1[j])
            spikes[j] = n.v
        neus1[i] = spikes
  
neus2 = {}
Iext2 = [30,37,5.3]
name2 = ["Classical","E4","interneurons"]
time2 = np.arange(1000,2000,dt)
for i in range(3):
    if(i < 2):
        n = IzhikevichNeuron(a = 0.01,b=0.2,c=-65,d=8)
        spikes = np.zeros(step)
        n.I_ext = Iext2[i]
        for j,t in enumerate(time2):
            n.update(dt,t)
            spikes[j] = n.v
        neus2[i] = spikes
    else:
        n = IzhikevichNeuron(a=0.1,b=0.2,c=-65,d=2)
        spikes = np.zeros(step)
        n.I_ext = Iext2[i]
        for j,t in enumerate(time2):
            n.update(dt,time2[j])
            spikes[j] = n.v
        neus2[i] = spikes
  
  
neus3 = {}
Iext3 = [30,45,7,5.5]
time3 = np.arange(2000,3000,dt)
name3 = ["Classical","C4","A5","interneurons"]
for i in range(4):
    if(i < 3):
        n = IzhikevichNeuron(a = 0.01,b=0.2,c=-65,d=8)
        spikes = np.zeros(step)
        n.I_ext = Iext3[i]
        for j,t in enumerate(time3):
            n.update(dt,t)
            spikes[j] = n.v
        neus3[i] = spikes
    else:
        n = IzhikevichNeuron(a=0.1,b=0.2,c=-65,d=2)
        spikes = np.zeros(step)
        n.I_ext = Iext3[i]
        for j,t in enumerate(time3):
            n.update(dt,time3[j])
            spikes[j] = n.v
        neus3[i] = spikes
  
neus4 = {}
Iext4 = [30,50,0,5.8]
time4 = np.arange(3000,4000,dt)
name4 = ["Classical","D4","E4","interneurons"]
for i in range(4):
    if(i < 3):
        n = IzhikevichNeuron(a = 0.01,b=0.2,c=-65,d=8)
        spikes = np.zeros(step)
        n.I_ext = Iext4[i]
        for j,t in enumerate(time4):
            n.update(dt,t)
            spikes[j] = n.v
        neus4[i] = spikes
    else:
        n = IzhikevichNeuron(a=0.1,b=0.2,c=-65,d=2)
        spikes = np.zeros(step)
        n.I_ext = Iext4[i]
        for j,t in enumerate(time4):
            n.update(dt,time4[j])
            spikes[j] = n.v
        neus4[i] = spikes
  
plt.figure()
for i in range(0,3):
    titles = "neuron:"+ name1[i]
    plt.subplot(4,4,i+1)
    plt.title(titles)
    if(name1[i] == "interneurons"):
        plt.plot(time1,neus1.get(i),color="dimgrey")
    else:
        plt.plot(time1,neus1.get(i),color="orange")
  
for i in range(0,3):
       
    plt.subplot(4,4,i+1+4)
    plt.title("neuron:"+ name2[i])
    if(name2[i] == "interneurons"):
        plt.plot(time2,neus2.get(i),color="dimgrey")
    else:
        plt.plot(time2,neus2.get(i),color="tomato")
   
for i in range(0,4):
    plt.subplot(4,4,i+1+8)
    plt.title("neuron:"+ name3[i])
    if(name3[i] == "interneurons"):
        plt.plot(time3,neus3.get(i),color="dimgrey")
    else:
        plt.plot(time3,neus3.get(i),color="teal")
  
for i in range(0,4):
    plt.subplot(4,4,i+1+12)
    plt.title("neuron:"+ name4[i])
    if(name4[i] == "interneurons"):
        plt.plot(time4,neus4.get(i),color="dimgrey")
    else:
        plt.plot(time4,neus4.get(i),color="slateblue")  
plt.show()

#-------------------------------------------------synaptic graph------------------------------------------------#
# input_path = "../midifiles/classic midi/"
# for composer in os.listdir(input_path):
#     print(composer)
#     dpath = os.path.join(input_path,composer)
#     if os.path.isdir(dpath):
#         for f in os.listdir(dpath):
#             fname = (os.path.join(dpath,f))
#             title = (f.split("."))[0]
#             brainEngine.rememberMusic(title, composer)
#             brainEngine.rememberMIDIMusic(title, composer, fname)






#def saveSynpases(brainEngine):
#     glink_f = open("goal_synapse.csv","w")
#     glink_f.write("pre,post,weight\n")
#     for g in brainEngine.cortex.ips.goals.groups.values():
#         for n in g.neurons:
#             for syn in n.synapses:
#                 #if(syn.weight == 0): continue
#                 strs = ""
#                 strs1 = str(syn.pre.layerIndex) + "_" + syn.pre.areaName[0] + "_" + str(syn.pre.groupIndex) + "_" + str(syn.pre.index) +","
#                 strs2 = str(syn.post.layerIndex) + "_" + syn.post.areaName[0] + "_" + str(syn.post.groupIndex) + "_" + str(syn.post.index) +"," + str(syn.weight)
#                 strs = strs1 + strs2 + "\n"
#                 glink_f.write(strs)
#     glink_f.close()
    
    
#     for trackIndex,tl in brainEngine.cortex.msm.sequenceLayers.items():
#         print(trackIndex)
#         if(trackIndex > 2):continue
#         for key,sl in tl.items():
#             print(key)
#             fn = str(trackIndex)+"_"+str(key)
#             plink_f = open(fn + "_synapse.csv","w")
#             plink_f.write("pre,post,weight\n")
#             for g in sl.groups.values():
#                 for n in g.neurons:
#                     for syn in n.synapses:
#                         if(syn.weight == 0): continue
#                         strs = ""
#                         w = syn.weight/5.0
#                         strs1 = str(syn.pre.layerIndex) + "_" + syn.pre.areaName[0] + "_" + str(syn.pre.groupIndex) + "_" + str(syn.pre.index) +","
#                         strs2 = str(syn.post.layerIndex) + "_" + syn.post.areaName[0] + "_" + str(syn.post.groupIndex) + "_" + str(syn.post.index) +"," + str(w)
#                         strs = strs1 + strs2 + "\n"
#                         plink_f.write(strs)       
# 
#             plink_f.close()


# musicName = "Sonate C major"
# fileName = "../midifiles/Sonate C major.mid"
# brainEngine.rememberMusic(musicName, "Mozart")
# brainEngine.rememberMIDIMusic(musicName, "Mozart", fileName)



# composer = "bach"
# input_path = "../midifiles/classic midi/"
# out_path = "../result_output/composing/"
# dpath = "../midifiles/classic midi/"+ composer
# # for dir in os.listdir(input_path):
# #     dpath = os.path.join(input_path,dir)
# if os.path.isdir(dpath):
#     for musicName in os.listdir(dpath):
#         fname = (os.path.join(dpath,musicName))
#         brainEngine.rememberMusic(musicName,composer)
#         brainEngine.rememberMIDIMusic(musicName, composer,fname)
#  
#  
# print("--------saving the synapses-----------")
#   
# saveSynpases(brainEngine)


# sns.set()
# synapticweights = pd.read_csv("1_T_synapse.csv")
# new_synweights = synapticweights.pivot("pre","post","weight")
# f,ax = plt.subplots(figsize=(4,4))
# sns.heatmap(new_synweights,cmap = "icefire", center = 200)
# plt.show()


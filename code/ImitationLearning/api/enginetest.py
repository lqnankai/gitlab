'''
Created on 2016.7.8

@author: liangqian
'''
from api.engineapi import EngineAPI

brain = EngineAPI()
brain.cortexInit()

music1 = "small stars"
dm1 = [17,18,17,18,21]
music2 = "happy songs"
dm2 = [17,19,20,21,22,23]
episodeNotes = [17,18]

# brain.rememberMusic(music1)
# for i,notename in enumerate(dm1):
#     order = i+1
#     brain.rememberANote(music1, notename, order)
#     
# brain.rememberMusic(music2)
# #print(len(brain.cortex.ips.goals.groups))
# for i,notename in enumerate(dm2):
#     order = i+1
#     brain.rememberANote(music2, notename, order)
# #brain.recallMusic(music1)
# #brain.recallMusic(music2)
# strs = brain.recallEpisode(episodeNotes)
# print(strs)
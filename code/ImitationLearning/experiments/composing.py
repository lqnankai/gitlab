'''
Created on 2020.07.08

@author: liangqian
'''
import os
#from GUI.globaldata import brainEngine
from GUI.globaldata import brainEngine

'''---------------------------------------------------------------------
                Composing the single track by all data
-------------------------------------------------------------------------'''
composerName = "bach"
#input_path = "../midifiles/classic midi/"
input_path = "../midifiles/test/"
out_path = "../result_output/composing/"
#dpath = "../midifiles/classic midi/"+ composerName
for dir in os.listdir(input_path):
    dpath = os.path.join(input_path,dir)
    if os.path.isdir(dpath):
        for musicName in os.listdir(dpath):
            fileName = (os.path.join(dpath,musicName))
            brainEngine.rememberMusic(musicName,dir)
            brainEngine.rememberMIDIMusic(musicName,dir, fileName)
#brainEngine.recallMusic('islamei.mid')
# episodeNotes = [58,58]
# brainEngine.recallEpisode(episodeNotes)
#brainEngine.saveModetoFile(composer)

# beginlist = {1:{'N':[60,67],'T':[0.5,0.25]},
#              2:{'N':[74,80],'T':[0.75,0.25]},
#              3:{'N':[65],'T':[1.0]}
#              }
# 
# for key, li in beginlist.items():
#     firstNote = li.get('N')
#     durations = li.get('T')
#     midic = brainEngine.generateEx_Nihilo(firstNote, durations, 20)
#     brainEngine.writeMIDIfile(out_path + composer+"_"+str(key), midic)
    
beginnotes = {1:[64,58],
              2:[64]}
begindurs = {1:[0.5,0.25],
             2:[0.5]}
lengths = [10,8]
genreName = "Baroque"
composerName = "Bach"
# #midic = brainEngine.generate2TrackMusic(beginnotes, begindurs, lengths)
#midic = brainEngine.generateEx_Nihilo(beginnotes.get(1), begindurs.get(1), 5)
#midic = brainEngine.generateEx_NihiloAccordingToGenre(genreName, beginnotes.get(1), begindurs.get(1), 5)
midic = brainEngine.generateEx_NihiloAccordingToComposer(composerName,beginnotes.get(1),begindurs.get(1),5)
brainEngine.writeMIDIfile2(composerName +"_twotrack", midic)

'''
Created on 2018.8.20

@author: liangqian
'''
import tornado.web
import pygame
#from GUI.globaldata import brainEngine
from midiprocess.readmidi import *
from midiprocess.play import *
from GUI.globaldata import brainEngine
from mido import Message, MidiFile, MidiTrack

class MidiControlHandler(tornado.web.RequestHandler):
    '''
    classdocs
    '''
    def get(self):
        
        currentState = self.get_argument("State")
        if(currentState == "Remember"):
            fileName = self.get_argument("MusicName")
            strs = fileName.split(".")
            musicName = strs[0]
            fileName = "../midifiles/" + fileName 
            brainEngine.rememberMusic(musicName,"Mozart")
            
            brainEngine.rememberMIDIMusic(musicName,"Mozart",fileName)
        
        if(currentState == "EpisodeRecall"):
            
            strs = self.get_argument("NoteID")
            ep = strs.split(",")
            episodeNotes = []
            for n in ep:
                episodeNotes.append(int(n))
            print(episodeNotes)
            result = brainEngine.recallEpisode(episodeNotes)
            for dic in result.values():
                fn = dic.get('goal')+'_ep.mid'
                mid = MidiFile()
                track = MidiTrack()
                mid.tracks.append(track)
                track.append(Message('program_change', program = 1,time = 0))
                for rn in (dic.get('rest')).values():
                    id = rn.get('id')
                    if(id == -1):continue
                    dur = int(rn.get('duration') * 480)
                    track.append(Message('note_on', note= id, velocity=64, time=0))
                    track.append(Message('note_off', note= id, velocity=64, time=dur))
                
                 
                print('Midi Generation finished!')
                # play
                freq = 44100
                bitsize = -16
                channels = 2
                buffer = 1024
                pygame.mixer.init(freq, bitsize, channels, buffer)
                pygame.mixer.music.set_volume(1)  
                clock = pygame.time.Clock()
                try:
                    pygame.mixer.music.load(fn)
                except:
                    import traceback
                    print(traceback.format_exc())
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    clock.tick(30)
            
        if(currentState == "Play"):
            flag = self.get_argument("Flag")
            if(flag == "1"):
                freq = 44100
                bitsize = -16
                channels = 2
                buffer = 1024
                pygame.mixer.init(freq, bitsize, channels, buffer)
                pygame.mixer.music.set_volume(1)  
                clock = pygame.time.Clock()
                try:
                    pygame.mixer.music.load("../midifiles/mz_331_3.mid")
                except:
                    import traceback
                    print(traceback.format_exc())
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    clock.tick(30)
            if(flag == "0"):
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.stop()
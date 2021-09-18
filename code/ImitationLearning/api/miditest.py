'''
Created on 2020.04.08

@author: liangqian
'''
from GUI.globaldata import brainEngine
from api.enginetest import episodeNotes
from mido import Message, MidiFile, MidiTrack
import pretty_midi
import pygame


musicName1 = "mz_331_3"
fileName1 = "../midifiles/mz_331_3.mid"

musicName2 = "Sonate C major"
fileName2 = "../midifiles/Sonate C major.mid"

episodeNotes = [72,76,79]
 
# brainEngine.rememberMusic(musicName1)
# brainEngine.rememberMIDIMusic(musicName1, fileName1)
#             
# brainEngine.rememberMusic(musicName2)
# brainEngine.rememberMIDIMusic(musicName2, fileName2)
# brainEngine.saveModetoFile('test')

brainEngine.loadModel('test_basic.csv', 'test_neuron.csv', 'test_synapse.csv')
#brainEngine.recallMusic(musicName2)


#brainEngine.recallEpisode(episodeNotes)
midic = brainEngine.generateEx_Nihilo([72,57],[1.0,0.25],10)
filePath = "../result_output/composing/"
brainEngine.writeMIDIfile(filePath + "test", midic)



def play_midi(file):
    
    freq = 44100
    bitsize = -16
    channels = 2
    buffer = 1024
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.set_volume(1)  
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(file)
    except:
        import traceback
        print(traceback.format_exc())
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(30)

     
# try:
#     play_midi(fileName1)
# except KeyboardInterrupt:
#     # if user hits Ctrl/C then exit
#     # (works only in console mode)
#     pygame.mixer.music.fadeout(1000)
#     pygame.mixer.music.stop()
#     raise SystemExit


def writemidi():
    mid = MidiFile()
    track = MidiTrack()
    track1= MidiTrack()
    mid.tracks.append(track)
    mid.tracks.append(track1)
    track.append(Message('note_on', note=64, velocity=64, time=0))
    track.append(Message('note_off', note=64, velocity=127, time=960))
    track.append(Message('note_on', note=60, velocity=64, time=0))
    track.append(Message('note_off', note=60, velocity=127, time=480))
    track.append(Message('note_on', note=71, velocity=64, time=0))
    track.append(Message('note_off', note=71, velocity=127, time=480))
    
    track1.append(Message('program_change', program = 1,time = 0))
    track1.append(Message('note_on', note=48, velocity=64, time=0))
    track1.append(Message('note_off', note=48, velocity=127, time=960))
    track1.append(Message('note_on', note=60, velocity=64, time=0))
    track1.append(Message('note_off', note=60, velocity=127, time=960))
    
    
    mid.save('new.mid')
 
 
#writemidi()   
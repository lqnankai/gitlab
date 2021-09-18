import pretty_midi

#pm = pretty_midi.PrettyMIDI("../midifiles/mz_331_3.mid")
pm = pretty_midi.PrettyMIDI("../midifiles/chpn_op10_e05.mid")
print (pm.instruments[0])
print(pretty_midi.note_number_to_name(60))
ins1 = pm.instruments[0]
count = 0
        
for note in ins1.notes[0:20]:
  
    count += 1
    start = pm.time_to_tick(note.start)
    end = pm.time_to_tick(note.end)
    print(str(count)+":(Pitch:"+str(note.pitch)+","+"start:"+str(start)+","+"end:"+str(end)+")")
     
print(pm.instruments[1])
for note in pm.instruments[1].notes[0:20]:
  
    count += 1
    start = pm.time_to_tick(note.start)
    end = pm.time_to_tick(note.end)
    print(str(count)+":(Pitch:"+str(note.pitch)+","+"start:"+str(start)+","+"end:"+str(end)+")")
from midiprocess.midi_event import MidiEvent
from midiprocess.meta_event import MetaEvent
from midiprocess.header import Header
from midiprocess.track import Track
from midiprocess.midifile import StandardMIDIFile


def generate_note_table():
        notes_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        midi_notes_table = {notes_names[i % 12] + str(i // 12): i for i in range(128)}
        return midi_notes_table


def play_notes(filename,notes,intervals,ppqn):
    filename = filename + '.mid'
    #table = generate_note_table()
    e = [MetaEvent(89, data=[2, 7, 0])]
    for i,n in enumerate(notes):
        ts = intervals[i]
        for note in n:
            e.append(MidiEvent(0, 144, 0, [note, 127]))
        for j,note in enumerate(n):
            e.append(MidiEvent(ts[j], 144, 0, [note, 0]))
    e.append(MetaEvent(47, 0))
    t = Track(e, 1)
    hdr = Header(0, 1, 480)
    smf = StandardMIDIFile(hdr, [t])
    f = open(filename, 'wb')
    f.write(smf.to_hex())
    f.close()

class StatusBytes:
    """Enumerating of status bytes with corresponding event types
    """
    meta = {0: 'Sequence Number', 1: 'Text', 2: 'Copyright', 3: 'Sequence / Track Name', 4: 'Instrument Name',
            5: 'Lyric', 6: 'Marker', 7: 'Cue Point', 8: 'Program Name', 9: 'Device Name', 32: 'MIDI Channel Prefix',
            33: 'MIDI Port', 47: 'End of Track', 81: 'Tempo', 84: 'SMPTE Offset', 88: 'Time Signature',
            89: 'Key Signature', 127: 'Sequencer Specific Event'}
    sysex = {240: 'Single (complete) SysEx messages', 247: 'Escape sequences'}
    midi = {128: 'Note off', 144: 'Note on', 160: 'Key pressure', 176: 'Control change', 192: 'Program change',
            208: 'Channel pressure', 224: 'Pitch wheel change'}

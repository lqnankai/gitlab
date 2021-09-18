from midiprocess.midi_exceptions import MidiError
from midiprocess.track import Track


class StandardMIDIFile:
    """Class MidiFormat describes Standard Midi File,
    in general, MidiFormat consists of Tracks list and Header
    """
    def __init__(self, header, tracks=[]):
        """
        :param header: midi header
        :param tracks: tracks of SMF
        :type header: Header
        :type tracks: list(Track)
        """
        if not header:
            raise MidiError(header, 'Header is empty')
        if not tracks:
            raise MidiError(tracks, 'Tracks list is empty')
        self.header = header
        self.tracks = tracks[:]

    def to_hex(self):
        """Get bytes representation of MidiFormat
        :return: converted to bytes file
        :rtype: bytes str (b'')
        """
        header = self.header.to_hex()
        tracks = b''.join(map(Track.to_hex, self.tracks))
        return header + tracks

    def __getitem__(self, item):
        return self.tracks[item]

    def __str__(self):
        header = str(self.header) + '\n'
        track = '\n'.join(map(str, self.tracks))
        return header + track






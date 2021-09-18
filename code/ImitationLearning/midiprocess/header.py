from midiprocess.midi_exceptions import MidiError
from struct import pack


class Header:
    """Class Header describes describes the structure of the standard midi file,
     i.e 'MThd', length, file format, number of tracks in file and Pulses Per Quarter Note(PPQN)
     """
    def __init__(self, file_format, ntracks, ppqn):
        """
        :param file_format: SMF type
        :param ntracks: number of tracks
        :param ppqn: tempo
        :type file_format: int
        :type ntracks: int
        :type ppqn: int
        :raise MidiError: Wrong file format
        :raise MidiError: Format 0 has only 1 track
        :raise MidiError: 16 tracks is maximum for SMF( 1 track for each channel)
        """
        if file_format not in [0, 1, 2]:
            raise MidiError(file_format, 'Wrong file format')
        if file_format == 0 and ntracks != 1:
            raise MidiError(file_format, 'Format 0 has only 1 track')
        if ntracks >= 31:
            raise MidiError(file_format, '16 tracks is maximum for SMF( 1 track for each channel)')
        self.mthd = b'MThd'
        self.length = 6
        self.file_format = file_format
        self.ntracks = ntracks
        self.ppqn = ppqn

    def to_hex(self):
        """Get bytes representation of the Header
        :return: header converted to bytes
        :rtype: bytes str (b'')
        """
        mthd = self.mthd
        params = pack('>LHHH', self.length, self.file_format, self.ntracks, self.ppqn)
        return mthd+params

    def __str__(self):
        return str((self.mthd, self.length, self.file_format, self.ntracks, self.ppqn))

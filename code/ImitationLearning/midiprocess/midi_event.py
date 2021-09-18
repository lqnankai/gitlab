from midiprocess.midi_exceptions import *
from midiprocess.event import Event
from midiprocess.status_bytes import StatusBytes


class MidiEvent(Event):
    """Class MidiEvent describes, obviously, a midievent such as 'Note on' or 'Note off'
    """
    def __init__(self, delta_time, status, channel_number=0, data=[]):
        """
        :param status: Midi event status byte
        :param delta_time: delta time
        :param channel_number: number of channel, default = 0
        :param data: data of the event, default = []
        :type status: int (byte)
        :type delta_time: int
        :type channel_number: int (0..15)
        :type data: list
        :raise ChannelError: Wrong channel number
        :raise StatusError: Wrong status byte
        :raise DataLengthError: Data not corresponding to event type
        :raise DataError: Wrong data
        """
        if not (0 <= channel_number <= 15):
            raise ChannelError(channel_number)
        if status not in StatusBytes.midi:
            raise StatusError(status)
        if (status in [192, 223] and len(data) != 1) or (status not in [192, 223] and len(data) != 2):
            raise DataLengthError(data)
        if max(data) > 127:
            raise DataError(data)
        Event.__init__(self,delta_time=delta_time, status=status + channel_number, data=data)

    def __str__(self):
        tup = self.delta_time, self.status, self.data, self.get_event_type
        result = 'delta_time = {}, status = {}, data = {}, event type: {}'.format(*tup)
        return Event.__str__(self) + result

    @property
    def get_event_type(self):
        """
        :return: Midi event type
        :rtype: str
        """
        return StatusBytes.midi[self.status & 240]


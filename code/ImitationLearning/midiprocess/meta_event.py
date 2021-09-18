from midiprocess.midi_exceptions import MidiError
from midiprocess.event import Event
from midiprocess.status_bytes import StatusBytes


class MetaEvent(Event):
    """Class MetaEvent describes, obviously, midi meta events
    unlike to class Event  has a fields length and event type
    """
    def __init__(self, event_type, delta_time=0, data=[]):
        """
        :param event_type: type of meta event
        :param delta_time: delta time, default = 0
        :param data: data of the event, default = []
        :type event_type: int (byte)
        :type delta_time: int
        :type data: list
        :raise  MidiError: Wrong event type for Meta event
        """
        if event_type not in StatusBytes.meta:
            raise MidiError(event_type, 'Wrong event type for Meta event')

        Event.__init__(self,delta_time=delta_time, status=255, data=data[:])
        self.event_type = event_type
        self.length = len(self.data)
        self.event = [
                        Event.variable_len(self.delta_time),
                        [self.status],
                        [self.event_type],
                        Event.variable_len(self.length),
                        self.data
                        ]

    def __str__(self):
        tup = self.delta_time, self.status, self.event_type, self.length, self.data, self.get_event_type
        result = 'delta_time = {}, status = {}, event_type = {}, length = {},  data = {}, event type: {} '.format(*tup)
        return Event.__str__(self) + result

    @property
    def get_event_type(self):
        """
        :return: Meta event type
        :rtype: str
        """
        return StatusBytes.meta[self.event_type]

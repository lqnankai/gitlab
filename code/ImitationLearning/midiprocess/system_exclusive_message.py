from midiprocess.midi_exceptions import StatusError
from midiprocess.event import Event
from midiprocess.status_bytes import StatusBytes


class SysExEvent(Event):
    """Class SysExEvent describes, obviously, midi system exclusive messages
    unlike to class Event  has a field length
    """
    def __init__(self, delta_time=0, status=240, data=[]):
        """
        :param status: System exclusive event status byte, default = 240
        :param delta_time: delta time, default = 0
        :param data: data of the event, default = []
        :type status: int (byte)
        :type delta_time: int
        :type data: list
        :raise StatusError: Wrong status byte
        """
        if status not in StatusBytes.sysex:
            raise StatusError(status)

        Event.__init__(self,delta_time=delta_time, status=status, data=data[:])
        self.length = len(self.data)
        self.event = [
                        Event.variable_len(self.delta_time),
                        [self.status],
                        Event.variable_len(self.length),
                        self.data
                      ]

    def __str__(self):
        tup = self.delta_time, self.status, self.length, self.data, self.get_event_type
        result = 'delta_time = {}, status = {}, length = {},  data = {}, event type: {}'.format(*tup)
        return Event.__str__(self) + result

    @property
    def get_event_type(self):
        """
        :return: System exclusive message type
        :rtype: str
        """
        return StatusBytes.sysex[self.status]


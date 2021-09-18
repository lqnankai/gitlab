from midiprocess.midi_exceptions import MidiError
from midiprocess.event import Event
from struct import pack


class Track:
    """Class Track describes midi track,
     in general class Track consists of Event's list and track header
    """
    def __init__(self, events, running_status_mode=True):
        """
        :param events: list of the Event's
        :param running_status_mode: running status mode on/off; default = True
        :type events: list[Event]
        :type running_status_mode: bool
        :raise MidiError: Events list is empty
        """
        if not events:
            raise MidiError(events, 'Events list is empty')
        self.header = b'MTrk'
        self.events = events[:]
        self.running_status_mode = running_status_mode
        self.length, self.bytes = self.length_and_bytes()

    def to_hex(self):
        """Get bytes representation of track
        :return:
        :rtype: bytes str (b'')
        """
        header = self.header
        length = pack('>L', self.length)
        events = self.bytes
        return header + length + events

    def length_and_bytes(self):
        """Because of the variable length value, we can not specify the length of the track without converting
        events list to a byte string
        :return: bytes representation of event's list and it's length
        :rtype: int, bytes str (b'')
        """
        if self.running_status_mode:
            byte_string = self.running_status()
        else:
            byte_string = b''.join(map(Event.to_hex, self.events))
        return len(byte_string), byte_string

    def running_status(self):
        """To save memory we can use a trick, calling 'running status', it means, that if several MidiEvent
        if several MidiEvent's with the same status byte are in progress, status byte required only for first event
        :return: the resulting bytes representation of Midi events in running status mode
        :rtype bytes str (b'')
        """
        byte_string = self.events[0].to_hex()   # get first event
        current_status = self.events[0].status  # get first event status
        for event in self.events[1:]:
            # does this Event is MidiEvent
            if current_status == event.status < 240:
                # Yes
                h = event.to_hex()
                delta_time = event.get_delta_time
                byte_string += delta_time + h[len(delta_time)+1:]
            else:
                # No
                byte_string += event.to_hex()
            # change current status
            current_status = event.status
        return byte_string

    @property
    def get_event(self):
        return self.events

    def __getitem__(self, item):
        return self.events[item]

    def __str__(self):
        header = 'MTrk length =  {}'.format(self.length) + '\n'
        events = '\n'.join(map(str, self.events))
        return header + events


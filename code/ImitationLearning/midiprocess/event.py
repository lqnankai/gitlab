from midiprocess.midi_exceptions import MidiError


class Event:
    """Class Event describes the general structure of all events in Midi protocol, this implementation implies that
    delta time is a part of each event, also all events have status byte and some portion of data
    """
    def __init__(self, delta_time, status, data=[]):
        """
        :param status: event status byte
        :param delta_time: delta time
        :param data: data of the event, default = []
        :type status: int (byte)
        :type delta_time: int
        :type data: list
        :raise MidiError: Wrong delta time value
        """
        if not (0 <= delta_time <= 4294967167):
            raise MidiError(delta_time, ' Wrong delta time value')
        self.delta_time = delta_time
        self.status = status
        self.data = self.str_to_int(data[:])
        self.event = [
                        self.variable_len(self.delta_time),
                        [self.status],
                        self.data
                      ]

    def to_hex(self):
        """Get bytes representation of event
        :return Event converted to bytes string
        :rtype: bytes str (b'')
        """
        b = b''.join(map(bytes, self.event))
        return b

    @staticmethod
    def str_to_int(data_with_str):
        """Converting all str data to int data
        :param data_with_str: some data with str values
        :type data_with_str: list
        :return data without str values
        :rtype: list
        """
        data = list(map(lambda x: ord(x) if isinstance(x, str) else x, data_with_str))
        return data

    @staticmethod
    def variable_len(time_or_len):
        """Convert int delta time or length to variable length quantity ( 1-4 bytes)
        :param time_or_len: delta time or length of event value
        :type time_or_len: int
        :return: converted to variable length quantity int value
        :rtype: bytes str (b'')
        """
        n = time_or_len
        variable_length = [n & 0x7f]
        n >>= 7
        for cnt in range(2):
            if n > 0:
                variable_length.append((n & 0x7f) | 0x80)
                n >>= 7
        byte_string = bytes(variable_length[::-1])
        return byte_string

    @property
    def get_delta_time(self):
        return bytes(self.event[0])

    def __str__(self):
        return self.__class__.__name__ + ' : '

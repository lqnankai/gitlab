class MidiError(Exception):
    def __init__(self, data, msg):
        self.data = data
        self.msg = msg

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.msg) + ': ' + str(self.data)


class DataLengthError(MidiError):
    def __init__(self, data):
        MidiError.__init__(self,data, ' Data not corresponding to event type')


class StatusError(MidiError):
    def __init__(self, status):
        MidiError.__init__(self,status, 'Wrong status byte')


class ChannelError(MidiError):
    def __init__(self, channel_number):
        MidiError.__init__(self,channel_number, 'Wrong channel number')


class DataError(MidiError):
    def __init__(self, data):
        MidiError.__init__(self,data, ' Wrong data')

class Room:
    def __init__(self, room_number, room_type):
        self._room_number = room_number
        self._room_type = room_type

    @property
    def room_number(self):
        return self._room_number

    @property
    def room_type(self):
        return self._room_type

    def __str__(self):
        return f"{self.room_number} - {self.room_type}"

    def __repr__(self):
        return self.__str__()
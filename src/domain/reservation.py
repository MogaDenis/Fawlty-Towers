from datetime import datetime


class Reservation:
    def __init__(self, number, room_number, family_name, number_of_guests, arrival, departure):
        self._number = number
        self._room_number = room_number
        self._family_name = family_name
        self._number_of_guests = number_of_guests
        self._arrival = arrival
        self._departure = departure

    @property
    def number(self):
        return self._number

    @property
    def room_number(self):
        return self._room_number

    @property
    def family_name(self):
        return self._family_name

    @property
    def number_of_guests(self):
        return self._number_of_guests

    @property
    def arrival(self):
        return self._arrival

    @property
    def departure(self):
        return self._departure

    def __str__(self):
        return f"{self.number} - {self.room_number} - {self.family_name} - {self.arrival.strftime('%d.%m')} - {self.departure.strftime('%d.%m')}"
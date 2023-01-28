import random
from domain.reservation import Reservation


class NoAvailableRoomException(Exception):
    pass


class ReservationService:
    def __init__(self, reservation_repo, room_repo):
        self._reservation_repo = reservation_repo
        self._room_repo = room_repo

    def generate_random_number(self):
        random_number = ""
        for _ in range(4):
            random_number += str(random.randint(0, 9))

        return random_number

    def search_available_room(self, room_type):
        available_rooms = self._room_repo.get_available_rooms()

        for room in available_rooms:
            if room.room_type == room_type:
                self._room_repo._available_rooms.remove(room)
                return room

        raise NoAvailableRoomException

    def delete_reservation(self, reservation_number):
        self._reservation_repo.delete_reservation(reservation_number)

    def add_reservation(self, reservation_data):
        """_summary_

        :param reservation_data: _description_
        """
        # We have to generate a random, unique ID for the new reservation. 
        used_numbers = []
        for reservation in self._reservation_repo:
            used_numbers.append(reservation.number)

        random_number = self.generate_random_number()

        while random_number in used_numbers:
            random_number = self.generate_random_number()

        family_name, room_type, guests, arrival, departure = reservation_data

        available_room = self.search_available_room(room_type)

        new_reservation = Reservation(random_number, available_room.room_number, family_name, guests, arrival, departure)

        self._reservation_repo.add_reservation(new_reservation)

        

        
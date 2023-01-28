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

    def search_rooms_available_in_interval(self, start_time, end_time):
        available_rooms = []
        for room in self._room_repo:
            available = True
            for reservation in self._reservation_repo:
                if reservation.room_number == room.room_number:
                    # Check if time intervals overlap.
                    if reservation.arrival <= start_time <= reservation.departure:
                        available = False
                    if reservation.arrival <= end_time <= reservation.departure:
                        available = False
                    if start_time <= reservation.arrival <= end_time:
                        available = False
                    if start_time <= reservation.departure <= end_time:
                        available = False

            if available:
                available_rooms.append(room)

        return available_rooms[:]

    def search_available_room(self, room_type, arrival, departure):
        # Search for rooms that match the type if there are reservations in the chosen interval. 
        for room in self._room_repo:
            if room.room_type == room_type:
                # Now check all reservations. 
                available = True
                for reservation in self._reservation_repo:
                    if room.room_number == reservation.room_number:
                        # Check if time intervals overlap.
                        if reservation.arrival <= arrival <= reservation.departure:
                            available = False
                        if reservation.arrival <= departure <= reservation.departure:
                            available = False
                        if arrival <= reservation.arrival <= departure:
                            available = False
                        if arrival <= reservation.departure <= departure:
                            available = False

                if available:
                    return room

        raise NoAvailableRoomException

    def delete_reservation(self, reservation_number):
        self._reservation_repo.delete_reservation(reservation_number)

    def add_reservation(self, reservation_data, test_state=False):
        """
            This method receives the reservation data, assigns a random number and an available room, creates the reservation object and adds it to the repository. 

        :param reservation_data: List of reservation info(family name, room type, number of guests, time of arrival and departure)
        :param test_state: If the method is under a test, it returns the reservation object, defaults to False
        :return: The reservation object only if put under unit test. 
        """
        # We have to generate a random, unique ID for the new reservation. 
        used_numbers = []
        for reservation in self._reservation_repo:
            used_numbers.append(reservation.number)

        random_number = self.generate_random_number()

        while random_number in used_numbers:
            random_number = self.generate_random_number()

        family_name, room_type, guests, arrival, departure = reservation_data

        available_room = self.search_available_room(room_type, arrival, departure)

        new_reservation = Reservation(random_number, available_room.room_number, family_name, guests, arrival, departure)

        self._reservation_repo.add_reservation(new_reservation, test_state)

        if test_state:
            return new_reservation

        

        
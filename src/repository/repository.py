from domain.room import Room
from domain.reservation import Reservation


class ReservationNotFoundException(Exception):
    pass


class DuplicateReservationException(Exception):
    pass


class ReservationRepoIterator:
    def __init__(self, repo):
        self._repo = repo
        self._index = 0 

    def __iter__(self):
        pass

    def __next__(self):
        if self._index >= len(self._repo):
            raise StopIteration

        self._index += 1

        return self._repo._list_of_reservations[self._index - 1]


class RoomRepoIterator:
    def __init__(self, repo):
        self._repo = repo
        self._index = 0 

    def __iter__(self):
        pass

    def __next__(self):
        if self._index >= len(self._repo):
            raise StopIteration

        self._index += 1

        return self._repo._list_of_rooms[self._index - 1]


class ReservationRepo:
    def __init__(self):
        self._list_of_reservations = []

    def __iter__(self):
        return ReservationRepoIterator(self)

    def __len__(self):
        return len(self._list_of_reservations)

    def get_all(self):
        return self._list_of_reservations[:]

    def add_reservation(self, new_reservation):
        for reservation in self:
            if new_reservation.number == reservation.number:
                raise DuplicateReservationException

        self._list_of_reservations.append(new_reservation)

    def delete_reservation(self, reservation_number):
        """
            This method deletes a reservation of which reservation number is given. 

        :param reservation_number: String. 
        :raises ReservationNotFoundException: If the reservation was not found.
        """

        found = False

        for i, reservation in enumerate(self):
            if reservation.number == reservation_number:
                self._list_of_reservations.pop(i)
                found = True
                break

        if not found:
            raise ReservationNotFoundException

    def load_file(self):
        # TODO
        open_file = open("reservations.txt", 'r')

        lines = open_file.readlines()

        list_of_rooms = []

        for line in lines:
            tokens = line.split(';')

            new_room = Room(tokens[0], tokens[1])

            list_of_rooms.append(new_room)

        return list_of_rooms[:]

    def save_file(self):
        pass


class RoomRepo:
    def __init__(self):
        self._list_of_rooms = self.load_file()
        self._available_rooms = self._list_of_rooms[:]

    def get_all(self):
        return self._list_of_rooms[:]

    def get_available_rooms(self):
        return self._available_rooms[:]

    def add_room(self):
        pass    

    def __len__(self):
        return len(self._list_of_rooms)

    def __iter__(self):
        return RoomRepoIterator(self)

    def load_file(self):
        open_file = open("rooms.txt", 'r')

        lines = open_file.readlines()

        list_of_rooms = []

        for line in lines:
            tokens = line.strip().split(';')

            new_room = Room(tokens[0], tokens[1])

            list_of_rooms.append(new_room)

        return list_of_rooms[:]


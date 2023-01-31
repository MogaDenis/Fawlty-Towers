from domain.room import Room
from domain.reservation import Reservation
from datetime import datetime


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
    def __init__(self, test_state=False):
        if not test_state:
            self._list_of_reservations = self.load_file()
        else:
            self._list_of_reservations = []

    def __iter__(self):
        return ReservationRepoIterator(self)

    def __len__(self):
        return len(self._list_of_reservations)

    def get_all(self):
        return self._list_of_reservations[:]

    def add_reservation(self, new_reservation, test_state=False):
        for reservation in self:
            if new_reservation.number == reservation.number:
                raise DuplicateReservationException

        self._list_of_reservations.append(new_reservation)

        if not test_state:
            self.save_file()

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
        open_file = open("src/reservations.txt", 'r')

        lines = open_file.readlines()

        list_of_reservations = []

        for line in lines:
            tokens = line.strip().split(';')

            new_reservation = Reservation(tokens[0], tokens[1], tokens[2], int(tokens[3]), datetime.strptime(tokens[4], "%d.%m"), datetime.strptime(tokens[5], "%d.%m"))

            list_of_reservations.append(new_reservation)

        open_file.close()

        return list_of_reservations[:]

    def save_file(self):
        open_file = open("src/reservations.txt", 'w')

        for reservation in self:
            open_file.write(str(reservation) + '\n')

        open_file.close()


class RoomRepo:
    def __init__(self):
        self._list_of_rooms = self.load_file()

    def get_all(self):
        return self._list_of_rooms[:]

    def __len__(self):
        return len(self._list_of_rooms)

    def __iter__(self):
        return RoomRepoIterator(self)

    def load_file(self):
        open_file = open("src/rooms.txt", 'r')

        lines = open_file.readlines()

        list_of_rooms = []

        for line in lines:
            tokens = line.strip().split(';')

            new_room = Room(tokens[0], tokens[1])

            list_of_rooms.append(new_room)

        open_file.close()

        return list_of_rooms[:]


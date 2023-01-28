import unittest
from domain.reservation import Reservation
from domain.room import Room
from repository.repository import ReservationRepo, RoomRepo, DuplicateReservationException, ReservationNotFoundException
from service.reservation_service import ReservationService
from datetime import datetime


class TestRepo(unittest.TestCase):
    def setUp(self):
        self.reservation_repo = ReservationRepo(test_state=True)
        self.room_repo = RoomRepo()

    def test_add_reservation(self):
        new_reservation = Reservation('1234', 1, 'Moga', 1, datetime.strptime("28.01", "%d.%m"), datetime.strptime("29.01", "%d.%m"))

        self.reservation_repo.add_reservation(new_reservation, test_state=True)

        self.assertEqual(new_reservation, self.reservation_repo._list_of_reservations[-1])

        self.assertRaises(DuplicateReservationException, self.reservation_repo.add_reservation, new_reservation, test_state=True)

    def test_delete(self):
        new_reservation = Reservation('1234', 1, 'Moga', 1, datetime.strptime("28.01", "%d.%m"), datetime.strptime("29.01", "%d.%m"))

        self.reservation_repo.add_reservation(new_reservation, test_state=True)

        self.reservation_repo.delete_reservation('1234')

        self.assertNotIn(new_reservation, self.reservation_repo._list_of_reservations)

        self.assertRaises(ReservationNotFoundException, self.reservation_repo.delete_reservation, '1234')


class TestService(unittest.TestCase):
    def setUp(self):
        self.reservation_repo = ReservationRepo(test_state=True)
        self.room_repo = RoomRepo()
        self.service = ReservationService(self.reservation_repo, self.room_repo)

    def test_add_reservation(self):
        reservation_data = ['Moga', 'single', 1, datetime.strptime("28.01", "%d.%m"), datetime.strptime("29.01", "%d.%m")]

        new_reservation = self.service.add_reservation(reservation_data, test_state=True)

        self.assertEqual(new_reservation, self.reservation_repo._list_of_reservations[-1])

        self.assertRaises(DuplicateReservationException, self.reservation_repo.add_reservation, new_reservation, test_state=True)

    def test_delete(self):
        reservation_data = ['Moga', 'single', 1, datetime.strptime("28.01", "%d.%m"), datetime.strptime("29.01", "%d.%m")]

        new_reservation = self.service.add_reservation(reservation_data, test_state=True)

        self.service.delete_reservation(new_reservation.number)

        self.assertNotIn(new_reservation, self.reservation_repo._list_of_reservations)

        self.assertRaises(ReservationNotFoundException, self.service.delete_reservation, '1234')


if __name__ == "__main__":
    unittest.main()
from datetime import datetime
from service.reservation_service import ReservationService, NoAvailableRoomException
from repository.repository import ReservationRepo, RoomRepo, ReservationNotFoundException


class InvalidInputException(Exception):
    pass


class ConsoleUI:
    def __init__(self):
        self.reservation_repo = ReservationRepo()
        self.room_repo = RoomRepo()
        self.reservation_service = ReservationService(self.reservation_repo, self.room_repo)

    def print_menu(self):
        print("\n\t~ Main Menu ~\n")
        print("1 - Create a reservation.")
        print("2 - Delete a reservation.")
        print("3 - Show available rooms in a time interval.")
        print("4 - Monthly report.")
        print("5 - Day of the week report.")
        print("6 - Show all rooms, available rooms, reservations")
        print("0 - Exit the application\n")

    def read_user_choice(self):
        user_choice = input(">> ").strip()

        if user_choice not in ['0', '1', '2', '3', '4', '5', '6']:
            raise InvalidInputException

        if user_choice == '4':
            raise NotImplementedError

        return user_choice

    def read_reservation_number(self):
        user_input = input("Enter the number of the reservation you want to remove: ").strip()

        if len(user_input) != 4:
            raise InvalidInputException

        return user_input

    def read_time_interval(self):
        time_interval = input("Enter the time interval(dd.mm-dd.mm): ").strip()
        tokens = time_interval.split('-')

        if len(tokens) != 2:
            raise ValueError

        start_time = datetime.strptime(tokens[0], "%d.%m")
        end_time = datetime.strptime(tokens[1], "%d.%m")

        return start_time, end_time

    def read_reservation_data(self):
        family_name = input("Family name: ").strip()
        room_type = input("Room type(single/double/family): ").strip().lower()
        guests = input("Number of guests: ").strip()
        arrival = input("Arrival time(day.month): ").strip()
        departure = input("Departure time(day.month): ").strip()

        if len(family_name) == 0:
            raise InvalidInputException

        if room_type not in ['single', 'double', 'family']:
            raise InvalidInputException

        if not guests.isnumeric():
            raise InvalidInputException

        arrival = datetime.strptime(arrival, "%d.%m")
        departure = datetime.strptime(departure, "%d.%m")

        return [family_name, room_type, guests, arrival, departure]

    def start(self):
        while True:
            self.print_menu()

            while True:
                try:
                    user_choice = self.read_user_choice()
                    break
                except InvalidInputException:
                    print("\nInvalid input!\n")
                except NotImplementedError:
                    print("\nFunctionality not implemented! :(\n")

            if user_choice == '0':
                break

            elif user_choice == '1':
                # Create a reservation. 
                try:
                    reservation_data = self.read_reservation_data()
                    self.reservation_service.add_reservation(reservation_data)
                except NoAvailableRoomException:
                    print("\nThere are no rooms available for this reservation.\n")
                except InvalidInputException:
                    print("\nInvalid input!\n")
                except ValueError:
                    print("\nInvalid input!\n")

            elif user_choice == '2':
                # Delete a reservation. 
                try:
                    reservation_number = self.read_reservation_number()
                    self.reservation_service.delete_reservation(reservation_number)
                except InvalidInputException:
                    print("\nInvalid input!\n")
                except ReservationNotFoundException:
                    print("\nThe reservation with the given number couldn't be found!\n")

            elif user_choice == '3':
                # Show available rooms. 
                try:
                    start_time, end_time = self.read_time_interval()
                    available_rooms = self.reservation_service.search_rooms_available_in_interval(start_time, end_time)

                    if len(available_rooms) != 0:
                        print("\n\tThe available rooms in the given time interval are:\n")
                        for room in available_rooms:
                            print(room)

                    else:
                        print("\n\tThere are no available rooms in the given time interval.\n")

                except ValueError:
                    print("\nInvalid input!\n")

            elif user_choice == '4':
                # Monthly report. 
                pass

            elif user_choice == '5':
                # Day of the week report. 
                days_report = self.reservation_service.days_of_week_report()
                print()
                for pair in days_report:
                    day, number_of_reservations = pair
                    print(f"{day} - {number_of_reservations} reservations")

            elif user_choice == '6':
                for reservation in self.reservation_repo:
                    print(reservation)

                print()

                for room in self.room_repo:
                    print(room)


from b_logic_layer.main_ll import Main_LL
from b_logic_layer.destination_ll import Destination_LL
from models.destinations_model import Destinations_Model
from datetime import datetime
from a_ui_layer.clear import clear


class Destination_UI:
    def __init__(self) -> None:
        self.main_ll = Main_LL()

    def display_destination_menu(self, next_num=None):
        """Make menu for destinations"""
        if next_num and len(next_num) >= 1:
            num = next_num[0]
        else:
            num = ""
        while num != "b":
            print(
                "________                  __  .__               __  .__                      "
            )
            print(
                "\______ \   ____   ______/  |_|__| ____ _____ _/  |_|__| ____   ____   ______"
            )
            print(
                " | |  |  \_/ __ \ /  ___|   __|  |/    \|__  \_   __\  |/  _ \ /    \ /  ___/"
            )
            print(
                " | |__/   \  ___/ \___ \ |  | |  |   |  \/ __ \|  | |  (  (_) )   |  |\___ \ "
            )
            print(
                "/_________/\___/ |_____/ |__| |__|___|__(______/__| |__|\____/|___|__|_____/"
            )

            print(
                "\n1. List destinations\n2. Add destination\n3. Modify destination"
            )  # Menu Commands

            print(
                "B. Go Back\nM. Main Menu\nS. Staffer Menu\nQ. Quit"
            )  # General Commands
            if not next_num:
                num = input("\nEnter number: ").lower().strip()
            else:
                next_num = None

            if num == "1":
                clear()
                self.get_all_destinations()
                input("Press any key to go back: ")
                clear()
            elif num == "2":
                clear()
                print(self.create_destination())
                input("Press any key to go back: ")
                clear()
            elif num == "3":
                clear()
                self.update_destination()
                input("Press any key to go back: ")
                clear()
            if num == "m":
                clear()
                return "m"
            elif num == "f":  # Flyer Menu
                clear()
                return "f"
            elif num == "s":
                clear()
                return "s"
            elif num == "q":
                clear()
                return "q"
            elif num == "b" or num == "0":
                clear()
                return 'b'

            elif not num in ['1','2','3','m','f','s','q','b','0']:
                input("Invalid input, please try again\nPress any button to continue")
                clear()
                next_num = None

    def create_destination(self):
        """
        1. Takes in input for a new destination
        2. returns the information to logic layer
        Allows the user to create a new destination.
        """
        country_v = False
        while country_v == False:
            print("\nAdd Destination")
            country = input("Country: ").strip()
            if len(country.split()) < 1:
                print("Country must be atleast one word")
                continue
            if not any(char.isalpha() for char in country):
                print("Country must only contain letters")
            else:
                country_v = True

        airport_v = False
        while airport_v == False:
            airport = input("Airport: ").strip()
            if len(airport.split()) > 1 or len(airport.split()) < 1:
                print("Airport must be one word")
                continue
            if not any(char.isalpha() for char in airport):
                print("Airport must only contain letters")
            else:
                airport_v = True

        duration_v = False
        while duration_v == False:
            flight_duration = input("Flight duration (HH:MM): ").strip()
            if not any(char.isdigit() for char in flight_duration):
                print("Flight Duration must only contain numbers")
                continue
            try:
                datetime.strptime(flight_duration, "%H:%M").time()
            except ValueError:
                print("Please use the correct format (HH:MM)")
            else:
                duration_v = True

        distance_v = False
        while distance_v == False:
            distance = input("Flight distance in kilometers: ").strip()
            if not any(char.isdigit() for char in distance):
                print("Distance must only contain numbers")
                continue
            else:
                distance_v = True

        contact_v = False
        while contact_v == False:
            contact = input("Destination emergency contact: ").strip()
            contact_v = self.contact_validation(contact)

        sos_v = False
        while sos_v == False:
            sos_num = input("Destination emergency number: ").strip()
            sos_v = self.sos_num_validation(sos_num)

        destination = Destinations_Model(
            country, airport, flight_duration, distance, contact, sos_num
        )
        clear()
        return self.main_ll.create_destination(destination)

    def update_destination(self):
        """
        1. Takes in input for an updated destination
        2. returns the information to the logic layer
        Allows the user to update a destination.
        """
        dest = self.get_a_destination()

        print("Update destination contact info:")
        contact_v = False
        while contact_v == False:
            contact = input("Contact: ").strip()
            if len(contact.split()) < 2:
                print("The Contacts name must contain a first and a last name")
                continue
            if any(char.isdigit() for char in contact):
                print("Contacts name cant contain any numbers")
            else:
                contact_v = True

        sos_v = False
        while sos_v == False:
            sos_num = input("Emergency number: ").strip()
            if any(char.isalpha() for char in sos_num):
                print("SOS Number must only contain numbers")
                continue
            if len(sos_num) < 7:
                print("SOS Numbers must contain atleast 7 numbers")
            else:
                sos_v = True

        dest.contact = contact
        dest.sos_num = sos_num
        ret = self.main_ll.update_dest(dest)
        clear()
        print(f"\n{ret}")
        if ret == "Destination modified successfully":
            print(dest)
        return

    def get_all_destinations(self):
        """
        1. Takes in input to get all destinations
        2. Returns a list of all destinations
        Allows the user to get a list of all destinations.
        """
        destinations = self.main_ll.get_all_dest()
        for num, dest in enumerate(destinations, start=1):
            print(f"{num}. {dest}")

        return destinations

    def get_a_destination(self):
        """returns a destination based on their number in a list."""
        print("Please pick destination number")
        destinations = self.get_all_destinations()
        error = True
        while error:
            try:
                i = int(input("Enter Number: ").strip())
                a_destination = destinations[i - 1]
                return a_destination

            except ValueError:
                print("\nNot a valid number, please try again")

            except IndexError:
                print("\Destination not found")

    def contact_validation(self, contact):
        if len(contact.split()) < 2:
            print("The Contacts name must contain a first and a last name")
            return False
        if not any(char.isalpha() for char in contact):
            print("Contacts name must only contain letters")
            return False

        return True

    def sos_num_validation(self, sos_num):
        if not any(char.isdigit() for char in sos_num):
            print("SOS Number must only contain numbers")
            return False
        if len(sos_num) < 7:
            print("SOS Number must contain minimum 7 numbers")
            return False

        return True

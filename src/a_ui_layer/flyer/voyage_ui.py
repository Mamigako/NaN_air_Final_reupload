from b_logic_layer.main_ll import Main_LL
from a_ui_layer.flyer.destination_ui import Destination_UI
from models.voyages_model import Voyages_Model
from datetime import timedelta
from datetime import datetime
from a_ui_layer.clear import clear

class Voyage_UI:
    def __init__(self) -> None:
        self.main_ll = Main_LL()

    def display_voyage_menu(self, next_num=None):
        if next_num and len(next_num) >= 1:
            num = next_num[0]
        else:
            num = ""
        while num != "0":
            print("____   ____                                         ")
            print("\   \ /   /___ ___ __ _____     _____  ____   ______")
            print(" \   Y   /  _ \   |  |\__  \   / __  \/ __ \ /  ___/")
            print("  \     (  (_) )___  | / __ \ / /_/  /  ___/ \___ \ ")
            print("   \___/ \____/ /____|(______|\___  / \___/  /____/ ")
            print("                             /_____/                ")

            print(
                "\n1. Create Voyage\n2. Make voyage recurring\n3. Get All Voyages\n4. Get Voyages on date\n5. Get voyages in week"
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
                print("____   ____                                         ")
                print("\   \ /   /___ ___ __ _____     _____  ____   ______")
                print(" \   Y   /  _ \   |  |\__  \   / __  \/ __ \ /  ___/")
                print("  \     (  (_) )___  | / __ \ / /_/  /  ___/ \___ \ ")
                print("   \___/ \____/ /____|(______|\___  / \___/  /____/ ")
                print("                             /_____/                ")

                print("\n1. Use existing voyage\n2. Create new voyage")
                choice = input("Enter number: ").lower().strip()
                print()
                if choice == "1":
                    voyage = self.get_a_voyage()
                    self.create_voyage(voyage)
                elif choice == "2":
                    self.create_voyage()
                elif choice == "q":
                    return
                clear()
            elif num == "2":
                clear()
                voyage_to_copy = self.get_a_voyage()
                if isinstance(voyage_to_copy,str):
                    continue
                self.make_recurring(voyage_to_copy)
                clear()
            elif num == "3":
                clear()
                self.get_all_voyages()
                continue_prompt = input("Press [Enter] to continue")
                clear()
            elif num == "4":
                clear()
                self.get_specific_day_voyage()
                continue_prompt = input("Press [Enter] to continue")
                clear()
            elif num == "5":
                clear()
                self.get_specific_week_voyage()
                continue_prompt = input("Press [Enter] to continue")
                clear()

            elif num == "b" or num == "0":  # Back
                clear()
                return 'b'
            elif num == "m":  # Main Menu
                clear()
                return "m"
            elif num == "f":  # Flyer Menu
                clear()
                return "f"
            elif num == "s":  # Staffer Menu
                clear()
                return "s"
            elif num == "q":  # Quit Program
                clear()
                return "q"

            else:
                input("Invalid input, please try again\nPress any button to continue")
                clear()
                next_num = None

    def create_voyage(self, voyage: Voyages_Model = None):
        """Allows the user to create a new voyage."""

        if voyage:  # Use existing voyage
            new_times = self.get_time_date()
            voyage.dates_and_times = new_times
            voyage.set_times()
            voy = voyage

        else:  # Create new voyage
            dest = Destination_UI().get_a_destination()
            print(f"\n{dest}\n")
            (
                out_dep_date,
                out_dep_time,
                in_dep_date,
                in_dep_time,
            ) = self.get_time_date()
            voy = Voyages_Model(
                destination=dest,
                dates_and_times=(out_dep_date, out_dep_time, in_dep_date, in_dep_time),
            )

        result, voyage = self.main_ll.create_voyage(voy)

        if voyage:
            print()
            print(result)
            print(voyage)

        else:
            print(f"\n{result}")

        continue_prompt = input("Press any key to go back")
        return

    def get_a_voyage(self):
        """returns a specific voyage"""
        voyages = self.get_all_voyages()
        if voyages:
            error = True
            while error:
                try:
                    choice = input(
                        "Which voyage would you like to update?\nPlease respond with voyage number or press 'b' to go back: "
                    ).strip()
                    print()
                    if choice.lower() == "b":
                        return 'b'

                    choice = int(choice)
                    if choice == 0:
                        raise ValueError
                    
                    voyage = voyages[choice - 1]
                    return voyage

                except ValueError:
                    print("\nNot a valid number, please try again")

                except IndexError:
                    print("\nVoyage not found")
        else:
            return

    def make_recurring(self, voyage):
        """Allows the user to copy a voyage multiple times"""
        td = timedelta(0)
        print(
            "How frequently should the voyage be repeated?\n1. Daily\n2. Weekly\n3. Monthly"
        )
        c = input().strip()
        if c == "q" or c == 'b':
            clear()
            return
        elif c == "1":
            td = timedelta(days=1)
        elif c == "2":
            td = timedelta(weeks=1)
        elif c == "3":
            td = timedelta(weeks=4)
        else:
            print("\nNot a valid number, please try again")

        how_often = input("How often should the voyage be repeated?").strip()
        if how_often.lower() == 'b':
            clear()
            return
        try:
            how_often = int(how_often)
        except ValueError:
            print("Invalid number")
            return
        for i in range(1, how_often + 1):
            d_date = str(voyage.times[0] + td)
            d_time = str(voyage.times[1])
            d_time = d_time[:5]
            a_date = str(voyage.times[2] + td)
            a_time = str(voyage.times[3])
            a_time = a_time[:5]
            v = Voyages_Model(
                destination=voyage.destination,
                dates_and_times=(d_date, d_time, a_date, a_time),
            )
            result, voyage = self.main_ll.create_voyage(v)
            if not voyage:
                print(result)
                return

        print("Voyages created successfully")
        continue_prompt = input("Press any key to go back")

    def get_all_voyages(self):
        """Allows the user to print out a numbered list of all voyages"""
        voyages = self.main_ll.get_all_voy()
        if voyages:
            print("\nList of Voyages")
            for num, voy in enumerate(voyages, start=1):
                print(f"{num}\n{voy}")
            return voyages
        else:
            print("\nNo Voyages to Show")

    def get_specific_day_voyage(self):
        """Allows the user to find a voyage on a specific day."""
        date = input(
            "Which date are you searching for? (yyyy-mm-dd)\nEnter Date: "
        ).strip()
        voy_on_date = self.main_ll.get_voy_on_date(date)
        if isinstance(voy_on_date, str):
            print(voy_on_date)
        else:
            for voy in voy_on_date:
                print(voy)

    def get_specific_week_voyage(self):
        """Allows the user to find a voyage in a specific week."""
        try:
            year, week = input("Please specify year and week (yyyy ww): ").strip().split()
        except ValueError: 
            return
        vou_in_week = self.main_ll.get_voy_in_week(year, week)
        if isinstance(vou_in_week, str):
            print(vou_in_week)
        else:
            print(f"\n\n\n\n\n\nFlights in week {week} in {year}:\n")
            for voy in vou_in_week:
                print(voy)

    def get_time_date(self):
        out_departure_date_v = False
        while out_departure_date_v == False:
            out_dep_date = input(
                "Input departure date for outgoing flight (yyyy-mm-dd): "
            ).strip()
            try:
                datetime.strptime(out_dep_date, "%Y-%m-%d").date()
            except ValueError:
                print("Please use the correct format (yyyy-mm-dd)")
            else:
                out_departure_date_v = True

        departure_time_v = False
        while departure_time_v == False:
            out_dep_time = input(
                "Input departure time for outgoing flight (hh:mm): "
            ).strip()
            try:
                datetime.strptime(out_dep_time, "%H:%M").time()
            except ValueError:
                print("Please use the correct format (hh:mm)")
            else:
                departure_time_v = True

        inc_departure_date_v = False
        while inc_departure_date_v == False:
            in_dep_date = input(
                "Input departure date for incoming flight (yyyy-mm-dd): "
            ).strip()
            try:
                datetime.strptime(in_dep_date, "%Y-%m-%d").date()
            except ValueError:
                print("Please use the correct format (yyyy-mm-dd)")
            else:
                inc_departure_date_v = True

        inc_departure_time_v = False
        while inc_departure_time_v == False:
            in_dep_time = input(
                "Input departure time for incoming flight (hh:mm): "
            ).strip()
            try:
                datetime.strptime(in_dep_time, "%H:%M").time()
            except ValueError:
                print("Please use the correct format (hh:mm)")
            else:
                inc_departure_time_v = True

        return (out_dep_date, out_dep_time, in_dep_date, in_dep_time)

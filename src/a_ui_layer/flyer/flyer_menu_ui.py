from a_ui_layer.flyer.voyage_ui import Voyage_UI
from a_ui_layer.flyer.destination_ui import Destination_UI
from a_ui_layer.clear import clear

class Flyer_Menu:
    def __init__(self) -> None:
        """"""

    def display_flyer_menu(self, next_num=None):
        if next_num and len(next_num) >= 1:
            num = next_num[0]
        else:
            num = 1
        while num != "b":
            print("___________ __                                                    ")
            print(
                "\_   _____/|  | ___ __  ___________      _____   ____   ____  __ __ "
            )
            print(
                " |   ___)  |  | |  |  |/ __ \_  __ \    /     \_/ __ \ /    \|  |  \ "
            )
            print(
                " |  |      |  |_\__   |  ___/|  | \/   |  Y Y  \  ___/|   |  \  |  /"
            )
            print(
                " |__|      |____/ |___|\___/ |__|      |__|_|__/\___/ |___|__/____/ "
            )
            print("\n1. Voyages\n2. Destinations")  # Menu Commands
            print("B. Go Back\nS. Staffer Menu\nQ. Quit\n")  # General commands
            if not next_num:
                num = input("Enter number: ").strip().lower()
            else:
                next_num = next_num[1:]
            if num == "1":
                clear()
                num = Voyage_UI().display_voyage_menu(next_num)
                clear()
                if num == 'b':
                    num = '0'
                    continue

            elif num == "2":
                clear()
                num = Destination_UI().display_destination_menu(next_num)
                if num == 'b':
                    num = '0'
                    continue

            elif num == "m":
                clear()
                return "m"
            if num == "q":
                clear()
                return "q"
            elif num == "b" or num == "0":
                clear()
                return
            elif num == "s":
                clear()
                return "s"

            else:
                input("Invalid input, please try again\nPress any button to continue")
                clear()
                next_num = None

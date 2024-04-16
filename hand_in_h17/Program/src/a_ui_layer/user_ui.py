from src.a_ui_layer.flyer.flyer_menu_ui import Flyer_Menu
from src.a_ui_layer.staffer_menu_ui import Staffer_Menu
from src.a_ui_layer.clear import clear


class User_UI:
    def __init__(self) -> None:
        self.display_user_ui()

    def display_user_ui(self, next_num=None):
        clear()
        num = "1"
        while num != "q":
            print(
                "                 __                                  __                                          __        "
            )
            print(
                "__  __  __ ____ |  |  _____  ____   _____   ____   _/  |_  ____     ____ _____    ____   _____  |__|______ "
            )
            print(
                "\ \/  \/ // __ \|  | /  ___\/  _ \ /     \_/ __ \  \   __\/  _ \   /   \ \__  \  /    \  \__  \ |  \_  __ \ "
            )
            print(
                " \      /\  ___/|  |_\  \__(  (_) )  Y Y  \  ___/   |  | (  (_) ) |   |  \/ __ \|   |  \  / __ \|  ||  | \/"
            )
            print(
                "  \_/\_/  \___/ |____/\___/ \____/|__|_|__/\___/    |__|  \____/  |___|__|(_____|___|__/ (____ _/__||__| \n"
            )
            print("Please choose your role\n")
            print("1. Flyer\n2. Staffer\nQ. Quit")

            num = input("\nEnter number: ").lower().strip()
            if len(num) > 1:
                next_num = num
                num = num[0]
                next_num = next_num[1:]

            if num == "1":
                clear()
                num = self.flyer_menu(next_num)

            elif num == "2":
                clear()
                num = self.staffer_menu(next_num)

            elif num == "q":
                clear()
                return

            while num == "f" or num == "s":
                clear()
                if num == "f":
                    num = self.flyer_menu()
                elif num == "s":
                    num = self.staffer_menu()

            if num == None:
                continue

            if num not in ["1", "2", "q", "f", "s", "b", "m"]:
                input("Invalid input, please try again\nPress any button to continue")
                clear()
                next_num = None

    def flyer_menu(self, next_num=None):
        return Flyer_Menu().display_flyer_menu(next_num)

    def staffer_menu(self, next_num=None):
        return Staffer_Menu().display_staffer_menu(next_num)

from src.a_ui_layer.flyer.voyage_ui import Voyage_UI
from src.b_logic_layer.main_ll import Main_LL
from src.models.employee_model import Employee_Model, Pilot_Model, Attendant_Model
from src.a_ui_layer.clear import clear


class Staffer_Menu:
    def __init__(self) -> None:
        self.main_ll = Main_LL()
        self.voyage_ui = Voyage_UI()

    def display_staffer_menu(self, next_num=None):
        if next_num and len(next_num) >= 1:
            num = next_num[0]
        else:
            num = ""

        while num != "q":
            clear()
            print(
                "  _________ __          _____  _____                                            "
            )
            print(
                " /   _____//  |______ _/ ____\/ ____\ ___________     _____   ____   ____  __ __ "
            )
            print(
                " \_____  \    __\__  \_   __\_   __\ / __ \_  __ \   /     \ / __ \ /    \|  |  \ "
            )
            print(
                " /        \|  |  / __ \|  |   |  |  \  ___/|  | \/  |  Y Y  \  ___/|   |  \  |  /"
            )
            print(
                "/_________/|__| (_____/|__|   |__|   \___  |__|     |__|_|__/\___/ |___|__/____/ "
            )
            print(
                "\n1. Staff Voyage\n2. All employees\n3. Search Employees\n4. Add employee\n5. Modify employee"
                "\n6. All staff not working on day x\n7. All staff working on day x and dest\n8. Pilots\n9. Attendants\n"
            )  # Menu Commands

            print("B. Go Back\nF. Flyer Menu\nQ. Quit\n")  # General Commands

            if not next_num:
                num = input("\nEnter number: ").lower().strip()
            else:
                next_num = None

            if num == "1":  # Staff Voyage
                still_adding = True
                while still_adding:
                    clear()
                    voyage = self.voyage_ui.get_a_voyage()

                    if not voyage:
                        continue_prompt = input("Press any key to go back")
                        break
                    elif isinstance(voyage, str):
                        if voyage == "b":
                            break

                    print(voyage)

                    # Show free employees
                    date = voyage.times[0]
                    voy_list = []
                    for voy in self.main_ll.get_all_voy():
                        if (
                            (date == voy.dates_and_times[0])
                            or (date == voy.dates_and_times[2])
                        ) and (voy.employees != ""):
                            voy_list.append(voy)

                    free_employees = self.get_empl_from_voy_bySSN(voy_list)

                    name_list = []
                    ssnlist = []

                    for empl in free_employees:
                        name_list.append(empl.name)

                    for empl in free_employees:
                        ssnlist.append(empl.SSN)

                    emp = False

                    while emp not in name_list and emp not in ssnlist:
                        print(
                            "What employee would you like to add to this flight? Press b to go back."
                        )

                        emp = input("Name or SSN: ")
                        if emp == "q" or emp == "b":
                            break

                        if emp not in name_list and emp not in ssnlist:
                            print("Invalid input! Please enter valid employee details.")

                    for e in free_employees:
                        if emp == e.name or emp == e.SSN:
                            if not self.main_ll.check_availability(e, voyage.times[0]):
                                print("Employee already assigned on that day")
                            else:
                                ret_string = self.main_ll.add_employee_to_voyage(
                                    voyage, e
                                )
                                print(ret_string)
                            break

                    continue_prompt = input("[b] to go back/[Enter] to continue:")
                    if continue_prompt.lower() == "b":
                        still_adding = False

            elif num == "2":  # All Employees
                clear()
                self.print_all_employees()

                continue_prompt = input("Press any key to go back")
                continue

            elif num == "3":  # Search Employees
                clear()
                choice = " "
                while choice.lower() != "b":
                    print("Search by:\n1.Name\n2.SSN\n")

                    print("[b] to go back")
                    choice = input("Enter your choice: ").strip()
                    if choice.lower() == "1" or choice.lower() == "2":
                        self.search_employee_name_SSN(choice)
                    else:
                        print("\ninvalid input try again\n")
                        continue

            elif num == "4":  # Add Employee
                clear()
                while True:
                    print("Choose employee type to add:\n ")
                    print("1. Pilot")
                    print("2. Attendant")
                    print("3. Exit")

                    choice = input("Enter your choice: ").strip()

                    if choice == "3":
                        break

                    elif choice != "1" and choice != "2":
                        print("Invalid input! Please enter a valid choice. ")

                    else:
                        employee_info = self.add_employee(choice)

                        print(self.main_ll.create_emp(employee_info))

                        continue_prompt = input("Press [Enter] to go back ")
                        break

                    continue

            elif num == "5":  # Update Employee
                clear()
                employees = self.main_ll.get_all_emp()

                for num, staff in enumerate(employees, start=1):
                    print(f"{num}. {staff}")

                employee_picked = False

                while not employee_picked:
                    employee_number = input(
                        "Select employee to update or [b] to go back: "
                    ).strip()
                    try:
                        employee_number = int(employee_number)
                        staff_to_change = employees[employee_number - 1]
                        employee_picked = True

                    except ValueError:
                        employee_number = employee_number.lower()
                        if employee_number == "b":
                            break
                        print("Invalid input! Please enter a number.\n")

                    except IndexError:
                        print(
                            f"Employee not found, please pick a number between 1 and {len(employees)}"
                        )
                if employee_number != "b":
                    print("\nSelected Employee: ")
                    print(staff_to_change)

                    employee_info = self.display_modify_employee_menu(staff_to_change)

                    result = self.main_ll.update_emp(employee_info)

                    if result == "b":
                        return

            elif num == "6":  # All staff not working on day x
                clear()
                date = input("\nEnter date to check(YYYY-MM-DD): ")
                voy_list = []
                for voy in self.main_ll.get_all_voy():
                    if (
                        (date == voy.dates_and_times[0])
                        or (date == voy.dates_and_times[2])
                    ) and (voy.employees != ""):
                        voy_list.append(voy)

                print(f"\n\n\nEmployees not working on {date}: ")
                print("-")
                self.get_empl_from_voy_bySSN(voy_list)
                continue_prompt = input("Press [Enter] to continue")

            elif num == "7":  # All staff working on day x and dest
                clear()
                date = input("\nEnter date to check(YYYY-MM-DD): ")

                all_employees = self.main_ll.get_all_emp()
                all_destinations = self.main_ll.get_all_dest()
                all_voyages = self.main_ll.get_all_voy()

                voyage_list = []
                employee_list = []

                for voyage in all_voyages:
                    if (
                        (date == voyage.dates_and_times[0])
                        or (date == voyage.dates_and_times[2])
                    ) and (voyage.employees != ""):
                        voyage_list.append(voyage)

                for voyage in voyage_list:
                    for employee_SSN in voyage.employees:
                        for employee in all_employees:
                            if isinstance(employee_SSN, str):
                                if employee.SSN == employee_SSN:
                                    employee_list.append((employee, voyage))
                            else:
                                if employee.SSN == employee_SSN.SSN:
                                    employee_list.append((employee, voyage))

                print(
                    f"\n\nList of employees working on {date} and their destinations: "
                )
                print()
                for employee, voyage in employee_list:
                    print(f"Employee: {employee.name}, Role: {employee.role}\n")
                    print(f"{voyage.destination}\n")

                continue_prompt = input("Press [Enter] to continue ")

            elif num == "8":  # Pilots
                clear()
                self.print_all_pilots()

                continue_prompt = input("Press any key to go back")
                continue

            elif num == "9":  # Attendants
                clear()
                self.print_all_attendants()
                continue_prompt = input("Press any key to go back")
                continue

            elif num == "b" or num == "0":  # Back
                clear()
                return
            elif num == "q":  # Quit program
                clear()
                return "q"
            elif num == "f":  # Flyer menu
                clear()
                return "f"

            else:
                input("Invalid input, please try again\nPress any button to continue")
                clear()
                next_num = None

    def display_modify_employee_menu(self, employee_object):
        """Allows the user to modify an employee."""
        choice = ""
        while choice.lower() != "b":
            print(
                "Choose what to update(Name and SSN cannot be changed, please create new employee)"
            )
            print("1.Address")
            print("2.GSM")
            print("3.Email")
            print("4.Home Phone")

            print("[b] to go back ")
            choice = input("Enter your choice: ").strip()
            choice_int = 0
            try:
                choice_int = int(choice)
            except ValueError:
                pass
            if choice_int in range(1, 5):
                employee_object = self.modify_employee(choice, employee_object)
            elif choice.lower() == "b":
                clear()
                return "b"
            else:
                print("Invalid input")

        return employee_object

    def modify_employee(self, choice, employee_object: Employee_Model):
        valid = False
        if choice == "1":
            print("\nPlease enter employee details.\n")
            while not valid:
                address = input("Address:").strip()
                if self.address_validation(address):
                    employee_object.address = address
                    message = self.main_ll.update_emp(employee_object)
                    valid = True

            print(message)
        elif choice == "2":
            print("\nPlease enter employee details.\n")
            while not valid:
                gsm = input("gsm:").strip()
                if self.gsm_validation(gsm):
                    employee_object.gsm = gsm
                    message = self.main_ll.update_emp(employee_object)
                    valid = True
            print(message)
        elif choice == "3":
            print("\nPlease enter employee details.\n")
            while not valid:
                email = input("Email:").strip()
                if self.email_validation(email):
                    employee_object.email = email
                    message = self.main_ll.update_emp(employee_object)
                    valid = True
            print(message)
        elif choice == "4":
            print("\nPlease enter employee details.\n")
            while not valid:
                home_phone = input("Home Phone:").strip()
                if self.home_phone_validation(home_phone):
                    employee_object.home_phone = home_phone
                    message = self.main_ll.update_emp(employee_object)
                    valid = True
            print(message)
        elif choice == "b":
            return
        else:
            print("invalid input!")

        return employee_object

    def add_employee(self, choice):
        """Allows the user to add an employee."""
        if choice.lower() == "pilot" or choice.lower() == "1":
            print("\nPlease enter pilot details.\n")

            name_v = False
            while name_v == False:
                name = input("Name: ").strip()
                name_v = self.name_validation(name)

            ssn_v = False
            while ssn_v == False:
                ssn = input("SSN: ").strip()
                ssn_v = self.ssn_validation(ssn)

            address_v = False
            while address_v == False:
                address = input("Address: ").strip()
                address_v = self.address_validation(address)

            gsm_v = False
            while gsm_v == False:
                gsm = input("GSM: ").strip()
                gsm_v = self.gsm_validation(gsm)

            email_v = False
            while email_v == False:
                email = input("Email: ").strip()
                email_v = self.email_validation(email)

            home_phone_v = False
            while home_phone_v == False:
                home_phone = input("Home phone(optional): ").strip()
                home_phone_v = self.home_phone_validation(home_phone)

            lever = False
            while lever == False:
                islead = input("Captain(y/n)?: ").strip()
                if islead.lower() == "y":
                    islead = True
                    lever = True
                elif islead.lower() == "n":
                    islead = False
                    lever = True
                else:
                    print("Invalid input, try again")

            role = "pilot"
            employee_info = Pilot_Model(
                name, ssn, role, islead, address, gsm, email, home_phone
            )
            return employee_info

        elif choice.lower() == "attendant" or choice.lower() == "2":
            lever = False
            print("\nPlease enter attendant details.\n")

            name_v = False
            while name_v == False:
                name = input("Name: ").strip()
                name_v = self.name_validation(name)

            ssn_v = False
            while ssn_v == False:
                ssn = input("SSN: ").strip()
                ssn_v = self.ssn_validation(ssn)

            address_v = False
            while address_v == False:
                address = input("Address: ").strip()
                address_v = self.address_validation(address)

            gsm_v = False
            while gsm_v == False:
                gsm = input("GSM: ").strip()
                gsm_v = self.gsm_validation(gsm)

            email_v = False
            while email_v == False:
                email = input("Email: ").strip()
                email_v = self.email_validation(email)

            home_phone_v = False
            while home_phone_v == False:
                home_phone = input("Home phone(optional): ").strip()
                home_phone_v = self.home_phone_validation(home_phone)

            lever = False
            while lever == False:
                islead = input("Lead Attendant(y/n)?: ").strip()
                if islead.lower() == "y":
                    islead = True
                    lever = True
                elif islead.lower() == "n":
                    islead = False
                    lever = True
                else:
                    print("Invalid input, try again")

            role = "attendant"
            employee_info = Attendant_Model(
                name, ssn, role, islead, address, gsm, email, home_phone
            )
            return employee_info
        else:
            return

    def print_all_pilots(self):
        """Prints a list of all pilots."""
        pilots = self.main_ll.get_all_pilots()
        if pilots == "No employees listed":
            print("No pilots listed")
        elif not pilots:
            print("No pilots listed")
        else:
            print("List of all pilots:\n")
            for pilot in self.main_ll.get_all_pilots():
                print(pilot)

    def print_all_attendants(self):
        """Prints a list of all flight attendants."""
        attendands = self.main_ll.get_all_attendants()
        if attendands == "No employees listed":
            print("No attendants listed")
        elif not attendands:
            print("No attendants listed")
        else:
            print("List of all attendants:\n")
            for attendant in self.main_ll.get_all_attendants():
                print(attendant)

    def print_all_employees(self):
        """Prints a list of all employees."""
        employees = self.main_ll.get_all_emp()
        if employees == "No employees listed":
            print(employees)
        else:
            print("List of all employees:\n")
            for object in self.main_ll.get_all_emp():
                print(object)

    def search_employee_name_SSN(self, choice):
        """Search for an employee with a given SSN."""
        num = True

        if choice == "1":
            while num == True:
                search_name = input("\nEnter employee name:").strip()
                for object in self.main_ll.get_all_emp():
                    if search_name.lower() == object.name.lower():
                        choice = " "
                        while choice.lower() != "q":
                            print(object)
                            print("1. Modify Employee info")
                            print("2. Get employee worklog")
                            print("Enter [b] to go back")

                            mod_del_empl = input("\nEnter your choice:").strip()
                            if mod_del_empl == "1":
                                object = self.display_modify_employee_menu(object)
                                if object == "b":
                                    return
                                print("[q] to exit")
                                print("[Enter] to continue\n")

                                choice = input("Enter your choice:").strip()
                                if choice.lower() == "q":
                                    self.main_ll.update_emp(object)
                                    break
                                elif choice.lower() == "b":
                                    clear()
                                    return
                                elif choice.lower() == "":
                                    continue
                            elif mod_del_empl == "2":
                                clear()
                                self.print_worklog(object)
                                return
                            elif mod_del_empl == "b":
                                return
                    else:
                        if (
                            object == self.main_ll.get_all_emp()[-1]
                            and object.name != search_name
                        ):
                            print("No such employee!")
                            break

        elif choice == "2":
            num = True
            while num == True:
                search_ssn = input("\nEnter employee SSN:").strip()
                num = self.ssn_validation(search_ssn)

                for object in self.main_ll.get_all_emp():
                    if search_ssn == object.SSN:
                        choice = " "
                        while choice.lower() != "q":
                            print(object)
                            print("1.Modify Employee info")
                            print("2.Delete Employee from file")

                            mod_del_empl = input("\nEnter your choice:").strip()
                            if mod_del_empl == "1":
                                object = self.display_modify_employee_menu(object)
                                print("[q] to exit")
                                print("[Enter] to continue\n")

                            elif mod_del_empl == "2":
                                clear()
                                self.print_worklog(object)
                                return

                            elif mod_del_empl == "b":
                                return

                            choice = input("Enter your choice:").strip()
                            if choice.lower() == "q":
                                self.main_ll.update_emp(object)
                                break
                            elif choice.lower() == "":
                                continue
                else:
                    if (
                        object == self.main_ll.get_all_emp()[-1]
                        and object.SSN != search_ssn
                    ):
                        print("No such employee!")
                        break

    def get_empl_from_voy_bySSN(self, voy_list):
        """Compares employees' SSN against a list of those who are working on a specific date..
        Prints out list of those not working on that date."""

        voy_SSN_list = []

        for voy in voy_list:
            for employee in voy.employees:
                if employee:
                    voy_SSN_list.append(employee.SSN)

        ret_list = []
        for object in self.main_ll.get_all_emp():
            if object.SSN not in voy_SSN_list:
                print(object)
                ret_list.append(object)

        return ret_list

    def print_worklog(self, employee: Employee_Model):
        """Prints a worklog for a specified employee."""
        try:
            year, week = (
                input("Please specify year and week (YYYY WW): ").strip().split()
            )
        except ValueError:
            print("Invalid Format")
            return
        try:
            year = int(year)
            week = int(week)
        except ValueError:
            print("Invalid format")
            return

        voyages = self.main_ll.get_voy_in_week_for_emp(employee, year, week)
        if not voyages:
            print("No voyages found")
            return
        elif isinstance(voyages, str):
            print(voyages)
            return
        print()
        for v in voyages:
            if v.manned:
                manned = "yes"
            else:
                manned = "no"
            print()
            print(
                f"{v.flights[0].flight_num}: Departs: {v.times[0]}, {v.times[1]}\t Returns: {v.times[2]}, {v.times[3]}\t Fully manned: {manned}"
            )
        print("\n")
        return

    # Input validation methods
    def name_validation(self, name: str) -> bool:
        """Returns True if the name is valid, otherwise False."""
        if len(name.split()) < 2:
            print("Invalid input: must give full name")
            return False
        for i in name:
            if not (i.isalpha() or i == " "):
                print("Invalid input: name must only contain letters")
                return False
        return True

    def ssn_validation(self, ssn: str) -> bool:
        """Returns True if the SSN is valid, otherwise False."""
        if not ssn.isnumeric():
            print("Invalid input, try again")
            return False
        if len(ssn) != 10:
            print("Invalid SSN, msut contain 10 numbers")
            return False

        return True

    def address_validation(self, address: str) -> bool:
        """Returns True if the address is valid, otherwise False."""
        split_address = address.split(" ")
        valid = False
        if len(split_address) < 2:
            print("Invalid input: Address must contain a street name and house number")
            return False
        elif split_address[0].isalpha() and split_address[-1].isnumeric():
            return True
        else:
            print("Invalid input: Address must contain a street name and house number")
            return False

    def gsm_validation(self, gsm: str) -> bool:
        """Returns True if the gsm is valid, otherwise False."""
        if len(gsm) < 7 or not gsm.isnumeric():
            print("Invalid input, number must contain at least 7 digits")
            return False

        return True

    def email_validation(self, email: str) -> bool:
        """Returns True if the email is valid, otherwise False."""
        if "@" in email and "." in email and email.split(".")[-1].isalpha():
            return True
        else:
            print("Invalid email, please try again.")
            return False

    def home_phone_validation(self, phone: str) -> bool:
        """Returns True if the home phone is either empty or valid, otherwise False."""
        if not phone:
            return True
        elif len(phone) < 7 or not phone.isnumeric():
            print("Invalid input: Home phone must contain at least 7 valid digits")
            return False

        return True

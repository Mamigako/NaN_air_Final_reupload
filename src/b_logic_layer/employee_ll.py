from c_storage_layer.main_io import Main_IO


class Employee_LL:
    """
    Logic class encapsulating employee operations, such as prompting creation, modification,
    and various reports.
    """

    def __init__(self, io: Main_IO) -> None:
        self.main_io = io

    def create_employee(self, employee_info):  
        """
        1. Receives employee info from UI.
        2. Formats the info.
        3. Sends it down to storage.
        """
        if self.verify_ssn_unique(employee_info.SSN):
            return self.main_io.add_employee_to_file(employee_info)
        else:
            return "There is already an employee with that SSN."

    def update_employee(self, employee_info):  
        """
        1. Receives employee info from UI.
        2. Formats the info.
        3. Sends it down to storage.
        """
        if isinstance(employee_info, str):
            if employee_info.lower() == "b":
                return "b"
        else:
            return self.main_io.update_employee(employee_info)

    def get_all_employees(self):  
        """
        1. Requests a list of all employees from storage.
        2. Checks whether empty or not
        2. Returns either employees or error to UI.
        """
        ret = self.main_io.get_all_employees()

        if ret:
            return tuple(ret)
        else:
            return "No employees listed"

    def check_availability(self, employee, date) -> bool:  
        """
        1. Receives employee name and datetime.
        2. Requests to storage if employee in Voyage/Flight within specified timeframe.
        3. Returns True or False.
        """

        all_voyages = self.main_io.get_voyages_io()
        selected_voyages = []
        for v in all_voyages:
            if v.times[0] == date:
                selected_voyages.append(v)

        available = True
        for v in selected_voyages:
            emp_list = [e.SSN for e in v.employees]
            if employee.SSN in emp_list:
                available = False

        return available

    def get_all_pilots(self):  
        """
        1. Receives prompt to get all pilots.
        2. Requests list of all pilots from storage.
        3. Returns said list.
        """
        all_employees = self.main_io.get_all_employees()

        ret_list = []

        for employee in all_employees:
            if employee.role == "pilot":
                ret_list.append(employee)

        if ret_list:
            return tuple(ret_list)
        else:
            return "No employees listed"

    def get_all_attendants(self):  
        """
        1. Receives prompt to get all attendants pilots.
        2. Requests list of all attendants from storage.
        3. Returns said list.
        """
        all_employees = self.main_io.get_all_employees()

        ret_list = []

        for employee in all_employees:
            if employee.role == "attendant":
                ret_list.append(employee)

        if ret_list:
            return tuple(ret_list)
        else:
            return "No employees listed"

    def verify_ssn_unique(self, ssn) -> bool:
        """
        Checks if a given SSN is unique, returns True if so, False otherwise.
        """
        employees = self.get_all_employees()
        unique = True
        for e in employees:
            if e.SSN == ssn:
                unique = False

        return unique

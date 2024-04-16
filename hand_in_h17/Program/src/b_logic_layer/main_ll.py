from src.b_logic_layer.employee_ll import Employee_LL
from src.b_logic_layer.voyage_ll import Voyage_LL
from src.b_logic_layer.destination_ll import Destination_LL
from src.b_logic_layer.flight_ll import Flight_LL
from src.c_storage_layer.main_io import Main_IO


class Main_LL:
    def __init__(self):
        io = Main_IO()
        self.employee_ll = Employee_LL(io)
        self.voyage_ll = Voyage_LL(io)
        self.destination_ll = Destination_LL(io)
        self.flight_ll = Flight_LL(io)

    def get_all_emp(self):
        return self.employee_ll.get_all_employees()

    def check_availability(self, employee, date) -> bool:
        return self.employee_ll.check_availability(employee, date)

    def get_all_pilots(self):
        return self.employee_ll.get_all_pilots()

    def get_all_attendants(self):
        return self.employee_ll.get_all_attendants()

    def create_emp(self, employee_info):
        return self.employee_ll.create_employee(employee_info)

    def update_emp(self, employee_info):
        return self.employee_ll.update_employee(employee_info)

    def get_all_voy(self):
        return self.voyage_ll.get_all_voyages()

    def get_voy_on_date(self, date):
        return self.voyage_ll.get_voyage_on_date(date)

    def get_voy_in_week(self, year, week):
        return self.voyage_ll.get_voyage_in_week(year, week)

    def create_voyage(self, voyage):
        return self.voyage_ll.create_voyage(self.flight_ll, voyage)

    def update_voyage(self, old_voyage, voyage):
        return self.voyage_ll.update_voyage(self.flight_ll, old_voyage, voyage)

    def create_destination(self, dest):
        return self.destination_ll.create_destination(dest)

    def get_dest(self):
        return self.destination_ll.get_destination()

    def update_dest(self, new_dest):
        return self.destination_ll.update_destination(new_dest)

    def get_all_dest(self):
        return self.destination_ll.get_all_destinations()

    def get_dest_by_country(self, country):
        return self.destination_ll.get_dest_by_country(country)

    def add_employee_to_voyage(self, voyage, employee):
        return self.voyage_ll.add_emp_to_voyage(voyage, employee)

    def get_voy_in_week_for_emp(self, employee, year, week):
        return self.voyage_ll.get_voyages_in_week_for_employee(employee, year, week)

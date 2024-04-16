from src.c_storage_layer.employee_io import Employee_IO
from src.c_storage_layer.voyage_io import Voyage_IO
from src.c_storage_layer.destination_io import Destination_IO
from src.c_storage_layer.flight_io import Flight_IO


class Main_IO:
    def __init__(self):
        self.employee_io = Employee_IO()
        self.destination_io = Destination_IO()
        self.flight_io = Flight_IO()
        self.voyage_io = Voyage_IO(
            self.employee_io, self.destination_io, self.flight_io
        )

    def get_all_employees(self):
        return self.employee_io.load_all_employees_from_file()

    def add_employee_to_file(self, employee_info):
        return self.employee_io.add_employee_to_file(employee_info)

    def update_employee(self, employee_info):
        return self.employee_io.update_employee(employee_info)

    def get_voyages_io(self):
        return self.voyage_io.load_all_voyages_from_file()

    def add_voyage(self, info):
        return self.voyage_io.add_voyage_to_file(info)

    def rebuild_voyage_list(self, voyage_list):
        return self.voyage_io.rebuild_file(voyage_list)

    def get_all_destinations(self):
        return self.destination_io.load_all_destination_from_file()

    def add_destination(self, dest):
        return self.destination_io.add_destination_to_file(dest)

    def modify_destination(self, old_dest, dest):
        return self.destination_io.modify_destination(old_dest, dest)

    def rebuild_dest_list(self, dest_tuple):
        return self.destination_io.rebuild_file(dest_tuple)

    def get_all_flights(self):
        return self.flight_io.load_all_flights_from_file()

    def add_flight(self, flight):
        return self.flight_io.add_flight_to_file(flight)

    def rebuild_flight_list(self, flight_list):
        return self.flight_io.rebuild_file(flight_list)

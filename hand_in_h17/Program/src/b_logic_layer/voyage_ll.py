from src.b_logic_layer.flight_ll import Flight_LL
from src.c_storage_layer.main_io import Main_IO
from src.models.voyages_model import Voyages_Model
from src.models.flights_model import Flights_Model
from datetime import datetime, timedelta


class Voyage_LL:
    def __init__(self, io: Main_IO) -> None:
        self.main_io = io

    def get_all_voyages(self):
        """
        1. Takes in voyage file
        2. Returns a list of voyages
        Iterates over every line in the file and returns a list of voyage objects"""
        ret = self.main_io.get_voyages_io()
        destinations = self.main_io.get_all_destinations()
        for v in ret:
            for d in destinations:
                if v.destination == d.id:
                    v.destination = d

        return ret

    def get_voyage_on_date(self, date) -> tuple[Voyages_Model]:
        """
        1. Takes in voyage file
        2. Returns a list of voyages on a date
        Iterates over every line in the file and returns a list of voyage objects on a date
        """

        # Validation
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date"

        voy_tup = self.get_all_voyages()
        ret = []
        for i in range(len(voy_tup)):
            fly_date = voy_tup[i].times[0]
            if fly_date == date:
                ret.append(voy_tup[i])

        if ret:
            return tuple(ret)
        else:
            return "No outbound flights on given day"

    def get_voyage_in_week(self, year, week):
        """
        1. Takes in voyage file
        2. Returns a list of voyages in a week
        Iterates over every line in the file and returns a list of voyage objects in a week
        """
        # Validation
        try:
            year, week = int(year), int(week)
        except ValueError:
            return "Not a valid year and week"

        voy_tup = self.get_all_voyages()
        start_date = datetime.fromisocalendar(year, week, 1).date()
        end_date = start_date + timedelta(days=6)

        ret = []
        for i in range(len(voy_tup)):
            fly_date = voy_tup[i].times[0]
            if start_date <= fly_date <= end_date:
                ret.append(voy_tup[i])

        if ret:
            return tuple(ret)
        else:
            return "No flights in given week"

    def create_voyage(self, logic_layer: Flight_LL, voyage: Voyages_Model):
        """
        1. Takes in voyage
        2. Appends voyage to file
        Takes in a voyage object and appends it to the file
        """
        # Validation
        failed, result = self.input_validation_create_voyage(voyage)
        if failed:
            return result, None
        logic_layer.register_flights(voyage.flights[0], voyage.flights[1])

        ret = self.main_io.add_voyage(voyage)
        return (ret, voyage)

    def input_validation_create_voyage(self, voyage: Voyages_Model) -> bool:
        today = datetime.today().date()
        if voyage.times[0] < today:
            return (
                True,
                "Invalid departure date, voyage must be scheduled in advance.",
            )
        elif (voyage.times[2] < voyage.times[0]) or (
            voyage.times[2] == voyage.times[0] and voyage.times[3] < voyage.times[1]
        ):
            return (True, "Departure flight must take place before return flight.")

        all_voyages = self.main_io.get_voyages_io()
        for v in all_voyages:
            if v.times[0] == voyage.times[0] and v.times[1] == voyage.times[1]:
                return "Error: Flight already scheduled at that time."
        return (False, "Voyage works")

    def add_emp_to_voyage(self, voyage: Voyages_Model, employee):
        """Adds the employee to the voyage"""
        emp_list = list(voyage.employees)
        emp_list.append(employee)
        voyage.employees = tuple(emp_list)

        voyage_list = self.get_all_voyages()
        new_voyages = []
        for v in voyage_list:
            if voyage == v:
                new_voyages.append(voyage)
            else:
                new_voyages.append(v)
        return_message = self.main_io.rebuild_voyage_list(new_voyages)
        if return_message == "File rebuilt successfully":
            return "Employee added to voyage"
        else:
            return "Error"

    def get_voyages_in_week_for_employee(self, employee, year: int, week: int):
        """Returns a tuple containing all voyages in a given week for a specified employee"""
        voy_in_week = self.get_voyage_in_week(year, week)
        if isinstance(voy_in_week, str):
            return voy_in_week

        voy_in_week = list(voy_in_week)
        relevant_voyages = []
        for v in voy_in_week:
            for e in v.employees:
                if isinstance(e, str):
                    if e == employee.SSN:
                        relevant_voyages.append(v)
                else:
                    if e.SSN == employee.SSN:
                        relevant_voyages.append(v)

        return tuple(relevant_voyages)

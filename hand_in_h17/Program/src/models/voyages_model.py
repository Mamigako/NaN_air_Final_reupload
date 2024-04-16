from datetime import datetime
from src.models.employee_model import Employee_Model, Pilot_Model, Attendant_Model
from src.models.flights_model import Flights_Model
from src.models.destinations_model import Destinations_Model


class Voyages_Model:
    """
    1. Takes in information about a voyage(2 flights)
    2. Returns the information as an object
    3. Defines them as object parameters
    destination is a Destination object
    dates_and_times is a tuple containing (out_date, out_time, in_date, in_time)
    """

    def __init__(
        self,
        destination: Destinations_Model,
        dates_and_times: tuple[str],
        flights: tuple[str] = ("", ""),
        employees: tuple[Employee_Model] = (),
    ) -> None:
        self.dates_and_times = dates_and_times
        self.times = ""
        self.set_times()

        self.destination = destination
        self.employees = employees
        self.flights = flights
        if type(flights[0]) != Flights_Model:
            self.create_flights()

        self.manned, p_num, p_lead, a_num, a_lead = self.fully_manned()

        self.p_num = p_num
        self.p_lead = p_lead
        self.a_num = a_num
        self.a_lead = a_lead

    def __str__(self) -> str:
        fli1, fli2 = self.flights
        flight1, flight2 = fli1.flight_num, fli2.flight_num
        date1, time1, date2, time2 = self.times
        times1 = f"{date1}, {time1}"
        times2 = f"{date2}, {time2}"

        employees = []
        for e in self.employees:
            if isinstance(e, str):
                employees.append(e)
            else:
                employees.append(e.name)
        employees = ", ".join(list(employees))

        not_manned_string = ""
        if not self.p_lead:
            not_manned_string += ", captain"
        if (self.p_num == 0 and not self.p_lead) or (self.p_num == 1 and self.p_lead):
            not_manned_string += f", pilot"
        if not self.a_lead:
            not_manned_string += ", lead attendant"
        not_manned_string = not_manned_string[2:]

        header_str = f' {"Destination":<20}{"Dep. Dates and Times":<25}{"Flights":<15} {"Manned":<5}'
        if self.manned:
            manned = "Yes"
        else:
            manned = f"No, requires {not_manned_string}"
        voy_str = f"{'':>3}{self.destination.airport:<15}{times1:<25}{flight1:^14}{manned:^15}\n{'':>18}{times2:<25}{flight2:^14}"
        emp_str = f" Employees\n{'':>3}{employees}"

        separator = 90 * "-"

        return f"{header_str}\n{voy_str}\n{emp_str}\n{separator}"

    def set_times(self) -> tuple[str]:
        try:
            self.times = (
                datetime.strptime(self.dates_and_times[0], "%Y-%m-%d").date(),
                datetime.strptime(self.dates_and_times[1], "%H:%M").time(),
                datetime.strptime(self.dates_and_times[2], "%Y-%m-%d").date(),
                datetime.strptime(self.dates_and_times[3], "%H:%M").time(),
            )
        except ValueError:
            self.times = ("", "", "", "")

    def create_flights(self) -> None:
        """Creates and saves 2 flights if they don't already exist."""
        flight1, flight2 = self.flights
        if isinstance(flight1, str):
            flight_num = flight1
        else:
            flight_num = flight1.id
        flight1 = Flights_Model(
            departure_date=self.times[0],
            departure_time=self.times[1],
            destination=self.destination.id,
            flight_num=self.flights[0],
        )

        if isinstance(flight2, str):
            flight_num = flight2
        else:
            flight_num = flight2.flight_num
        flight2 = Flights_Model(
            departure_date=self.times[2],
            departure_time=self.times[3],
            origin=self.destination.id,
            flight_num=self.flights[1],
        )
        self.flights = (flight1, flight2)

    def fully_manned(self) -> bool:
        """Checks if the voyage is sufficiently manned. Returns True if it is, otherwise False."""
        if self.employees == "":
            return False

        p_lead = False
        a_lead = False
        p_num = 0
        a_num = 0
        for e in self.employees:
            if isinstance(e, Pilot_Model):
                p_num += 1
                if e.islead:
                    p_lead = True
            if isinstance(e, Attendant_Model):
                a_num += 1
                if e.islead:
                    a_lead = True
        if p_lead and a_lead and p_num > 1 and a_num > 0:
            return True, p_num, p_lead, a_num, a_lead
        else:
            return False, p_num, p_lead, a_num, a_lead

    def __eq__(self, other) -> bool:
        return self.times == other.times and self.destination.id == other.destination.id

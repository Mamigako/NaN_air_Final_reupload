from datetime import datetime
from src.c_storage_layer.main_io import Main_IO
from src.models.flights_model import Flights_Model


class Flight_LL:
    def __init__(self, io: Main_IO) -> None:
        self.main_io = io

    def register_flights(self, flight_out: Flights_Model, flight_in: Flights_Model):
        """
        1. Takes in flight
        2. Validates flight attributes
        Takes in a flight object, gives it a flight number and sends it to the file or raises an error.
        """

        flight_list = self.get_flights_on_date(flight_out.departure_date)
        i = 0
        for f in flight_list:
            # Check flight numbers to generate flight number

            dest_id = int(f.flight_num[2:4])
            if int(f.destination) == dest_id:
                i += 2

        all_flight_nums = [f.flight_num for f in self.get_all_flights()]
        flight_out.make_flight_id(i)
        flight_in.make_flight_id(i + 1)

        # Ensures each flight number is unique
        # (Otherwise possibility of identical flight numbers if two voyages to the same destination
        # have outgoing flights on different days but return flights on the same day)

        self.main_io.add_flight(flight_out)
        self.main_io.add_flight(flight_in)
        return

    def get_all_flights(self):
        """
        1. Calls for information from the io layer
        2. Returns a tuple of flights
        """
        return self.main_io.get_all_flights()

    def get_flights_on_date(self, date) -> tuple[Flights_Model] | str:
        """
        1. Takes in flight file
        2. Returns a list of flights on a date
        Iterates over every line in the file and returns a list of flight objects on a date
        """

        flight_tup = self.main_io.get_all_flights()
        ret = []

        for flight in flight_tup:
            if flight.departure_date == date:
                ret.append(flight)
        return ret

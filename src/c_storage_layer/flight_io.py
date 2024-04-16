from datetime import datetime
from csv import DictWriter, DictReader
from models.flights_model import Flights_Model


class Flight_IO:
    def __init__(self):
        self.file_path = "c_storage_layer/storage/flights.csv"
        self.fieldnames = [
            "dep_date",
            "dep_time",
            "origin",
            "destination",
            "flight_num",
        ]

    def load_all_flights_from_file(self) -> tuple[Flights_Model]:  
        """
        1. Takes in flight file
        2. Returns a list of flights
        Returns all flights from a given file as a tuple.
        """
        ret = []
        with open(self.file_path, newline="", encoding="utf-8") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                ret.append(
                    Flights_Model(
                        departure_date=datetime.strptime(row[self.fieldnames[0]], "%d-%m-%y").date(),
                        departure_time=datetime.strptime(row[self.fieldnames[1]], "%H:%M").time(),
                        origin=row[self.fieldnames[2]],
                        destination=row[self.fieldnames[3]],
                        flight_num=row[self.fieldnames[4]],
                    )
                )
        return tuple(ret)

    def add_flight_to_file(self, flight: Flights_Model) -> str:
        """
        1. Takes in flight
        2. Adds he flight to a file
        Takes in a flight object and appends it to the file
        """
        with open(self.file_path, "a", newline="", encoding="utf-8") as csvfile:
            writer = DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(
                {
                    "flight_num": flight.flight_num,
                    "dep_date": flight.departure_date.strftime("%d-%m-%y"),
                    "dep_time": flight.departure_time.strftime("%H:%M"),
                    "origin": flight.origin,
                    "destination": flight.destination,
                }
            )

            return "Flight saved Successfully."

    def rebuild_file(self, flight_list):
        """Takes a list of flights as an argument and rebuilds the file from that list for the purposes of making modifications.
        WARNING: erases the existing file, use with caution."""
        with open(self.file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(
                {
                    "flight_num": "flight_num",
                    "dep_date": "dep_date",
                    "dep_time": "dep_time",
                    "origin": "origin",
                    "destination": "destination",
                }
            )
            for flight in flight_list:
                writer.writerow(
                    {
                        "flight_num": flight.flight_num,
                        "dep_date": flight.departure_date,
                        "dep_time": flight.departure_time,
                        "origin": flight.origin,
                        "destination": flight.destination,
                    }
                )

            return "File rebuilt successfully"

from src.models.destinations_model import Destinations_Model
from datetime import datetime


class Flights_Model:
    """
    1. Takes in information about a flight
    2. Returns the information as an object
    3. Defines them as object parameters
    """

    def __init__(
        self,
        departure_date: str,
        departure_time: str,
        origin: str = "00",
        destination: str = "00",
        flight_num: str = "",  # Added in logic layer if created by user, declared here if building from file
    ) -> None:
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        self.departure_time = departure_time
        self.flight_num = flight_num

    def __str__(self):
        return f"Departure Date: {self.departure_date} \nDeparture Time: {self.departure_time} \nDestination: {self.destination}"

    def fill_flight(self) -> None:
        if self.origin == "Iceland":
            self.origin = Destinations_Model(
                "Iceland",
                "Keflavík",
                self.destination.flight_duration,
                self.destination.distance,
                self.destination.contact,
                self.destination.sos_num,
                id="00",
            )

        elif self.destination == "Iceland":
            self.destination = Destinations_Model(
                "Iceland",
                "Keflavík",
                self.origin.flight_duration,
                self.origin.distance,
                self.origin.contact,
                self.origin.sos_num,
                id="00",
            )

    def make_flight_id(self, number_of_flight: int) -> str:
        """
        Flight id = _ _ _ _ _
        Company NA_ _ _
        Destination _ _XX_
        Flight per day to/from dest _ _ _ _X
        """
        if self.destination == "00":
            id = self.origin
        else:
            id = self.destination

        self.flight_num = f"NA{id}{number_of_flight}"

    def definition(self) -> list[str]:
        """
        Used to convert a flight to a list, to be stored in a csv file.
        Can later be replaced once flight ID is implemented.
        """
        return [
            self.origin,
            self.destination,
            self.departure_date.__str__(),
            self.departure_time.__str__(),
        ]

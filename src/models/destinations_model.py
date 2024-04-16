from datetime import datetime
from datetime import timedelta


class Destinations_Model:
    """
    1. Takes in information about a destination
    2. Returns the information as an object
    3. Defines them as object parameters
    """

    def __init__(
        self,
        country: str,
        airport: str,
        flight_duration: str,
        distance: float,
        contact: str,
        sos_num: str,
        id: str = "",  # Created in the logic layer before saving
    ) -> None:
        self.country = country
        self.airport = airport
        self.flight_duration = flight_duration
        self.distance = distance
        self.contact = contact
        self.sos_num = sos_num
        self.id = id

    def __str__(self):
        airport = f"Airport is {self.airport}"
        country = f"Country is {self.country}"
        duration = f"Flight duration is (HH:MM) {self.flight_duration}"
        distance = f"Flight distance is {self.distance} km"
        contact = f"Emergency contact is {self.contact}"
        sos = f"SOS phone number is {self.sos_num}"

        separator = 50 * "-"

        ret = f"Destination:\n {airport}\n {country}\n {duration}\n {distance}\n {contact}\n {sos}\n{separator}"

        return ret

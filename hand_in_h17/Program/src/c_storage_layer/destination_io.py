from csv import DictWriter, DictReader
from src.models.destinations_model import Destinations_Model

class Destination_IO:
    def __init__(self):
        self.file_path = "src/c_storage_layer/storage/destinations.csv"
        self.fieldnames = [
            "id",
            "country",
            "airport",
            "flight_duration",
            "distance",
            "contact",
            "sos_num",
        ]

    def load_all_destination_from_file(self) -> tuple[Destinations_Model]:
        """
        1. Takes in destination file
        2. Returns a list of destinations
        Returns all destinations from a given file
        """
        ret = []
        with open(self.file_path, newline="", encoding="utf-8") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                ret.append(
                    Destinations_Model(
                        row["country"],
                        row["airport"],
                        row["flight_duration"],
                        row["distance"],
                        row["contact"],
                        row["sos_num"],
                        row["id"],
                    )
                )
        return tuple(ret)

    def add_destination_to_file(self, dest: Destinations_Model):
        """ "
        1. Takes in destination
        2. Adds destination to a file
        Takes in a destination object and appends it to the file
        """
        with open(self.file_path, "a", newline="", encoding="utf-8") as csvfile:
            writer = DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(
                {
                    "id": dest.id,
                    "country": dest.country,
                    "airport": dest.airport,
                    "flight_duration": dest.flight_duration,
                    "distance": dest.distance,
                    "contact": dest.contact,
                    "sos_num": dest.sos_num,
                }
            )

            return "Destination saved Successfully."

    def modify_destination(
        self, old_dest: Destinations_Model, dest: Destinations_Model
    ):
        """
        1. Takes in destination
        2. Modifies destination in files
        Fetches the destination object from the file and modifies it
        """
        ret_list = []
        reader = 0

        with open(self.file_path, mode="r+", newline="", encoding="utf-8") as csvfile:
            reader = DictReader(csvfile)
            writer = DictWriter(csvfile, fieldnames=self.fieldnames)
            rows = [
                {
                    "id": "id",
                    "country": "country",
                    "airport": "airport",
                    "flight_duration": "flight_duration",
                    "distance": "distance",
                    "contact": "contact",
                    "sos_num": "sos_num",
                }
            ]
            for row in reader:
                if row["airport"] == dest.airport:
                    row["id"] = (dest.id,)
                    row["country"] = dest.country
                    row["airport"] = dest.airport
                    row["flight_duration"] = dest.flight_duration
                    row["distance"] = dest.distance
                    row["contact"] = dest.contact
                    row["sos_num"] = dest.sos_num
                rows.append(row)

            csvfile.seek(0)
            writer.writerows(rows)
            csvfile.truncate()

        return "Destination modified successfully."

    def rebuild_file(self, destinations: tuple[Destinations_Model]):
        """Takes a list of destinations as an argument and rebuilds the file from that list for the purposes of making modifications.
        WARNING: erases the existing file, use with caution."""
        with open(self.file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(
                {
                    "id": "id",
                    "country": "country",
                    "airport": "airport",
                    "flight_duration": "flight_duration",
                    "distance": "distance",
                    "contact": "contact",
                    "sos_num": "sos_num",
                }
            )
            for dest in destinations:
                writer.writerow(
                    {
                        "id": dest.id,
                        "country": dest.country,
                        "airport": dest.airport,
                        "flight_duration": dest.flight_duration,
                        "distance": dest.distance,
                        "contact": dest.contact,
                        "sos_num": dest.sos_num,
                    }
                )

            return "File rebuilt successfully"

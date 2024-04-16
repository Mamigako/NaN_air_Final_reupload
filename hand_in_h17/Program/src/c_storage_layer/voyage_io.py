from csv import DictWriter, DictReader
from datetime import datetime
from src.models.voyages_model import Voyages_Model
from src.models.employee_model import Employee_Model
from src.c_storage_layer.flight_io import Flight_IO
from src.c_storage_layer.destination_io import Destination_IO
from src.c_storage_layer.employee_io import Employee_IO


class Voyage_IO:
    def __init__(self, employee_io, destination_io, flight_io) -> tuple:
        self.file_path = "src/c_storage_layer/storage/voyages.csv"
        self.employee_io: Employee_IO = employee_io
        self.destination_io: Destination_IO = destination_io
        self.flight_io: Flight_IO = flight_io

    def load_previous_voyages_from_file(self) -> tuple[Voyages_Model]:
        """Load previous voyages from the file and returns them as a tuple."""
        ret_list = []
        with open(self.file_path, newline="", encoding="utf-8") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                ret_list.append(
                    Voyages_Model(
                        destination=row["destination"],
                        flights=(row["flight1"], row["flight2"]),
                        employees=row["employees"],
                        dates_and_times=(
                            row["departure_date"],
                            row["departure_time"],
                            row["arrival_date"],
                            row["arrival_time"],
                        ),
                    )
                )

        ret_tup = tuple(ret_list)
        return ret_tup

    def load_all_voyages_from_file(self) -> tuple[Voyages_Model]:
        """Loads all voyages from the file and returns them as a tuple."""
        ret_list = []
        employee_tuple = self.employee_io.load_all_employees_from_file()
        destination_tuple = self.destination_io.load_all_destination_from_file()
        flight_tuple = self.flight_io.load_all_flights_from_file()

        with open(self.file_path, newline="", encoding="utf-8") as csvfile:
            reader = DictReader(csvfile)

            greatest_length = max(
                len(employee_tuple), len(destination_tuple), len(flight_tuple)
            )

            for row in reader:
                dest = row["destination"]
                fli1 = row["flight1"]
                fli2 = row["flight2"]
                emps = row["employees"]
                emps = emps.split(";")

                for i in range(greatest_length):
                    try:
                        if dest == destination_tuple[i].id:
                            dest = destination_tuple[i]
                    except IndexError:
                        pass

                    try:
                        if fli1 == flight_tuple[i].flight_num:
                            fli1 = flight_tuple[i]
                        elif fli2 == flight_tuple[i].flight_num:
                            fli2 = flight_tuple[i]
                    except IndexError:
                        pass
                    try:
                        """
                        Checks emp SSN from file against empl database.
                        If SSN stored in voy file matches SSN from emp
                        file emp object from file is stored in Voyage
                        """
                        if (e := employee_tuple[i].SSN) in emps:
                            emps[emps.index(e)] = employee_tuple[i]

                    except IndexError:
                        pass

                # Ensure there aren't any empty strings in the employee tuple
                for e in emps:
                    if isinstance(e, str):
                        emps.remove(e)
                emps = tuple(emps)

                ret_list.append(
                    Voyages_Model(
                        destination=dest,
                        flights=(fli1, fli2),
                        employees=emps,
                        dates_and_times=(
                            row["departure_date(yyyy-mm-dd)"],
                            row["departure_time(hh:mm)"],
                            row["arrival_date(yyyy-mm-dd)"],
                            row["arrival_time(hh:mm)"],
                        ),
                    )
                )

        ret_tup = tuple(ret_list)
        return ret_tup

    def add_voyage_to_file(self, voyage: Voyages_Model, file_path: str = None):
        """Appends a voyage to the file."""
        destination = voyage.destination.id
        d_date = str(voyage.times[0])
        d_time = str(voyage.times[1])
        d_time = d_time[:5]  # (hh:mm:ss) -> (hh:mm)
        a_date = str(voyage.times[2])
        a_time = str(voyage.times[3])
        a_time = a_time[:5]
        flight1 = voyage.flights[0].flight_num
        flight2 = voyage.flights[1].flight_num
        if not file_path:
            file_path = self.file_path

        emps = []
        if voyage.employees:
            emps = [e.SSN for e in voyage.employees]
            emps = ";".join(emps)

        with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "departure_date(yyyy-mm-dd)",
                "departure_time(hh:mm)",
                "arrival_date(yyyy-mm-dd)",
                "arrival_time(hh:mm)",
                "flight1",
                "flight2",
                "employees",
                "destination",
            ]
            emps = ";".join(emps)
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(
                {
                    "departure_date(yyyy-mm-dd)": d_date,
                    "departure_time(hh:mm)": d_time,
                    "arrival_date(yyyy-mm-dd)": a_date,
                    "arrival_time(hh:mm)": a_time,
                    "flight1": flight1,
                    "flight2": flight2,
                    "employees": emps,
                    "destination": destination,
                }
            )

            return "Voyage saved Successfully"

    def rebuild_file(self, voy_list):
        """Takes a list of voyages as an argument and rebuilds the file from that list for the purposes of making modifications.
        WARNING: erases the existing file, use with caution."""
        with open(self.file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = DictWriter(
                csvfile,
                fieldnames=[
                    "departure_date(yyyy-mm-dd)",
                    "departure_time(hh:mm)",
                    "arrival_date(yyyy-mm-dd)",
                    "arrival_time(hh:mm)",
                    "flight1",
                    "flight2",
                    "employees",
                    "destination",
                ],
            )
            writer.writerow(
                {
                    "departure_date(yyyy-mm-dd)": "departure_date(yyyy-mm-dd)",
                    "departure_time(hh:mm)": "departure_time(hh:mm)",
                    "arrival_date(yyyy-mm-dd)": "arrival_date(yyyy-mm-dd)",
                    "arrival_time(hh:mm)": "arrival_time(hh:mm)",
                    "flight1": "flight1",
                    "flight2": "flight2",
                    "employees": "employees",
                    "destination": "destination",
                }
            )
            for voyage in voy_list:
                destination = voyage.destination.id
                d_date = str(voyage.times[0])
                d_time = str(voyage.times[1])
                d_time = d_time[:5]  # (hh:mm:ss) -> (hh:mm)
                a_date = str(voyage.times[2])
                a_time = str(voyage.times[3])
                a_time = a_time[:5]
                flight1 = voyage.flights[0].flight_num
                flight2 = voyage.flights[1].flight_num
                if not self.file_path:
                    file_path = self.file_path

                emps = []
                if voyage.employees:
                    for e in voyage.employees:
                        if isinstance(e, str):
                            emps.append(e)
                        else:
                            emps.append(e.SSN)
                    emps = ";".join(emps)
                writer.writerow(
                    {
                        "departure_date(yyyy-mm-dd)": d_date,
                        "departure_time(hh:mm)": d_time,
                        "arrival_date(yyyy-mm-dd)": a_date,
                        "arrival_time(hh:mm)": a_time,
                        "flight1": flight1,
                        "flight2": flight2,
                        "employees": emps,
                        "destination": destination,
                    }
                )

            return "File rebuilt successfully"

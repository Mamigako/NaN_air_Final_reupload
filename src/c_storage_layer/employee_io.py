from csv import DictReader, DictWriter
from models.employee_model import Employee_Model, Pilot_Model, Attendant_Model


class Employee_IO:
    def __init__(self):
        self.file_path = "c_storage_layer/storage/employees.csv"
        self.fieldnames = [
            "name",
            "SSN",
            "role",
            "islead",
            "address",
            "gsm",
            "email",
            "home_phone",
        ]

    def load_all_employees_from_file(self) -> tuple[Employee_Model]:  
        """
        1. Takes in employee file
        2. Returns a list of employee objects
        iterates over every line in the file and creates an employee object with line contents
        """
        ret = []
        with open(self.file_path, newline="", encoding="utf-8") as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                # Convert string to boolean
                if row["islead"] == "True":
                    islead = True
                else:
                    islead = False

                try:
                    if row["role"] == "pilot":
                        ret.append(
                            Pilot_Model(
                                row["name"],
                                row["SSN"],
                                row["role"],
                                islead,
                                row["address"],
                                row["gsm"],
                                row["email"],
                                row["home_phone"],
                            )
                        )
                    elif row["role"] == "attendant":
                        ret.append(
                            Attendant_Model(
                                row["name"],
                                row["SSN"],
                                row["role"],
                                islead,
                                row["address"],
                                row["gsm"],
                                row["email"],
                                row["home_phone"],
                            )
                        )
                except KeyError:
                    pass

        return tuple(ret)

    def add_employee_to_file(
        self, employee: Employee_Model or Pilot_Model or Attendant_Model
    ):  
        """
        1. Takes in employee
        2. Adds employee to file
        Takes in a employee object and appends it to the file
        """
        with open(self.file_path, "a", newline="", encoding="utf-8") as csvfile:
            writer = DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(
                {
                    "name": employee.name,
                    "SSN": employee.SSN,
                    "role": employee.role,
                    "islead": employee.islead,
                    "address": employee.address,
                    "gsm": employee.gsm,
                    "email": employee.email,
                    "home_phone": employee.home_phone,
                }
            )

            return "Employee saved!"

    def update_employee(self, employee: Pilot_Model or Attendant_Model):  

        """
        1. Takes in employee
        2. Modifies employee in files
        Fetches the destination object from the file and modifies it
        """
        ret_list = []
        reader = 0

        with open(self.file_path, mode="r+", newline="", encoding="utf-8") as csvfile:
            reader = DictReader(csvfile)
            writer = DictWriter(csvfile, fieldnames=self.fieldnames)
            rows = [
                {
                    "name": "name",
                    "SSN": "SSN",
                    "role": "role",
                    "islead": "islead",
                    "address": "address",
                    "gsm": "gsm",
                    "email": "email",
                    "home_phone": "home_phone",
                }
            ]
            for row in reader:
                if row["name"] == employee.name:
                    row["SSN"] = employee.SSN
                    row["role"] = employee.role
                    row["islead"] = employee.islead
                    row["address"] = employee.address
                    row["gsm"] = employee.gsm
                    row["email"] = employee.email
                    row["home_phone"] = employee.home_phone
                rows.append(row)

            csvfile.seek(0)
            writer.writerows(rows)
            csvfile.truncate()

        return "Employee modified successfully."
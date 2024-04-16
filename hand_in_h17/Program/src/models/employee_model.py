class Employee_Model:
    """
    1. Takes in information about an employee
    2. Returns the information as an object
    3. Defines them as object parameters
    """

    def __init__(
        self,
        name: str,
        SSN: str,
        role: str,
        islead=False,
        address="",
        gsm="",
        email="",
        home_phone="",
    ) -> None:
        self.name = name
        self.SSN = SSN
        self.role = role
        self.islead = islead
        self.address = address
        self.gsm = gsm
        self.email = email
        self.home_phone = home_phone

    def __str__(self):

        if (self.role == "attendant") and self.home_phone and (self.islead == True):
            header = f'{"Name":<20}{"Role":<20}{"SSN":<20}{"Address":<20}{"GSM Number":<20}{"Email":<35}'
            empl_str = f"{self.name:<20}{'Lead Attendant':<20}{self.SSN:<20}{self.address:<20}{self.gsm:<20}{self.email:<35}"
            h_phone = f"Home Phone: {self.home_phone}"
            h_seperator = len(h_phone) * "_" + "_"
            separator = len(empl_str) * "-"
            return f"{header}\n{empl_str}\n{h_seperator}\n{h_phone}\n{separator}"
    
        elif (self.role == "attendant") and (self.islead == True):
            header = f'{"Name":<20}{"Role":<20}{"SSN":<20}{"Address":<20}{"GSM Number":<20}{"Email":<35}'
            empl_str = f"{self.name:<20}{'Lead Attendant':<20}{self.SSN:<20}{self.address:<20}{self.gsm:<20}{self.email:<35}"
            separator = len(empl_str) * "-"
            return f"{header}\n{empl_str}\n\n{separator}"

        elif self.home_phone and (self.islead == False):
            header = f'{"Name":<20}{"Role":<20}{"SSN":<20}{"Address":<20}{"GSM Number":<20}{"Email":<35}'
            empl_str = f"{self.name:<20}{self.role.capitalize():<20}{self.SSN:<20}{self.address:<20}{self.gsm:<20}{self.email:<35}"
            h_phone = f"Home Phone: {self.home_phone}"
            h_seperator = len(h_phone) * "_" + "_"
            separator = len(empl_str) * "-"
            return f"{header}\n{empl_str}\n{h_seperator}\n{h_phone}\n{separator}"

        elif (self.role == "pilot") and self.home_phone and (self.islead == True):
            header = f'{"Name":<20}{"Role":<20}{"SSN":<20}{"Address":<20}{"GSM Number":<20}{"Email":<35}'
            empl_str = f"{self.name:<20}{'Captain':<20}{self.SSN:<20}{self.address:<20}{self.gsm:<20}{self.email:<35}"
            h_phone = f"Home Phone: {self.home_phone}"
            h_seperator = len(h_phone) * "_" + "_"
            separator = len(empl_str) * "-"
            return f"{header}\n{empl_str}\n{h_seperator}\n{h_phone}\n{separator}"

        elif (self.role == "pilot") and self.islead == True:
            header = f'{"Name":<20}{"Role":<20}{"SSN":<20}{"Address":<20}{"GSM Number":<20}{"Email":<35}'
            empl_str = f"{self.name:<20}{'Captain':<20}{self.SSN:<20}{self.address:<20}{self.gsm:<20}{self.email:<35}"
            separator = len(empl_str) * "-"
            return f"{header}\n{empl_str}\n\n{separator}"

        else:
            header = f'{"Name":<20}{"Role":<20}{"SSN":<20}{"Address":<20}{"GSM Number":<20}{"Email":<35}'
            empl_str = f"{self.name:<20}{self.role.capitalize():<20}{self.SSN:<20}{self.address:<20}{self.gsm:<20}{self.email:<35}"
            separator = len(empl_str) * "-"
            return f"{header}\n{empl_str}\n\n{separator}"


class Pilot_Model(Employee_Model):
    def __init__(
        self,
        name: str,
        SSN: str,
        role="pilot",
        islead=False,
        address="",
        gsm="",
        email="",
        home_phone="",
    ) -> None:
        super().__init__(name, SSN, role, islead, address, gsm, email, home_phone)

    def modify_license(self, islead):
        self.islead = islead


class Attendant_Model(Employee_Model):
    def __init__(
        self,
        name: str,
        SSN: str,
        role="attendant",
        islead=False,
        address="",
        gsm="",
        email="",
        home_phone="",
    ) -> None:
        super().__init__(name, SSN, role, islead, address, gsm, email, home_phone)

    def modify_license(self, islead):
        self.islead = islead

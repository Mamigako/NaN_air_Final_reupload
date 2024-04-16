from c_storage_layer.main_io import Main_IO
from models.destinations_model import Destinations_Model
from datetime import datetime


class Destination_LL:
    def __init__(self, io: Main_IO) -> None:
        self.main_io = io

    def create_destination(self, dest: Destinations_Model):
        id = len(self.main_io.get_all_destinations())
        dest.id = f"{id:02d}"
        # If all was successfull
        msg = self.main_io.add_destination(dest)
        output = msg + "\n" + str(dest)
        return output

    def get_destination(self, search):
        """
        1. Takes in destination file
        2. Returns a destination
        iterates over every line in the file and returns a destination object
        """

        dest_list = self.main_io.get_all_destinations()
        for item in dest_list:
            if item.airport == search:
                return item
        return "Error: No destination found"

    def update_destination(self, new_dest):  
        """
        1. Takes in destination
        2. Updates destination in file
        Fetches the destination object from the file and modifies it
        """

        dest_list = list(self.main_io.get_all_destinations())
        for i in range(len(dest_list)):
            if dest_list[i].airport == new_dest.airport:
                dest_list[i] = new_dest
        self.main_io.rebuild_dest_list(tuple(dest_list))
        return "Destination modified successfully"

    def get_all_destinations(self):
        """
        Returns a tuple of all destinations except Iceland, 
        which is used for return flights but shouldn't be listed as a destination.
        """
        destinations = list(self.main_io.get_all_destinations())
        for d in destinations:
            if d.id == "00":
                destinations.remove(d)
                break
        return tuple(destinations)

    def get_dest_by_country(self, country: str):
        """
        1. Takes in destination file
        2. returns a list of destinations in a country
        Iterates over every line in the file and returns a list of destination objects in a country
        """
        if not country.isalpha():
            return "Invalid country. Country names can only contain letters."

        dest_list = self.main_io.get_all_destinations()
        ret_list = []
        for dest in dest_list:
            if dest.country.lower() == country.lower():
                ret_list.append(dest)

        return ret_list

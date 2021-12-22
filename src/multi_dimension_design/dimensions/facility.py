#############################
#   Imports and Contants    #
#############################

# Python modules
from dataclasses import dataclass

# Local module
from src.multi_dimension_design.dimensions.location_grid import Location_Grid
from src.multi_dimension_design.dimensions.utils_ import FACILITY
from src.multi_dimension_design.dimensions.location import Location

def read_zip_codes():
    with open('../data/Zip_Codes.csv') as f:
        zip_codes = []
        for zip_info in f.readlines()[1:]:
            zip_info = zip_info.split('"')[1:]
            poligon_vec = zip_info[0]
            att_vec = zip_info[1].split(',')
            poligon = Location.poligon_str_2_poligon(poligon_vec)
            new_zip_info = [poligon] + att_vec
            zip_codes.append(new_zip_info)
        return zip_codes


zip_codes = read_zip_codes()


class Facility:
    """Representing the location region dimension in multimodal design"""
    original_key: str
    name: str
    type: FACILITY
    location: str

    def __init__(self, original_key, name, facility_type, location):
        self.original_key = original_key
        self.name = name
        self.facility_type = facility_type

        temp_coords = [location.x, location.y]
        zip_info = Location.extract_zip_info(zip_codes, temp_coords)

        try:
            temp_location = Location(original_key, temp_coords, zip_info)
        except:
            print("----------------------------" + name + "-----------------------------------")

        self.location = str(temp_location)


    def __str__(self):
        return f'{self.original_key},' \
               f'"{self.name}",' \
               f'{self.facility_type.value},' \
               f'{self.location}'


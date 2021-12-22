#############################
#   Imports and Contants    #
#############################

# Python modules
from dataclasses import dataclass

# Local module
from src.multi_dimension_design.dimensions.location import Location
from src.multi_dimension_design.dimensions.utils_ import FACILITY
from src.multi_dimension_design.dimensions.date import Date


@dataclass
class Vax_Site:
    """Representing the location region dimension in multimodal design"""
    original_key: str
    name: str
    facility_type: FACILITY
    location: str
    begin_date: str
    end_date: str


    def __init__(self, original_key, name, facility_type, location, begin_date, end_date):
        self.original_key = original_key
        self.name = name
        self.facility_type = facility_type
        self.location = str(location)
        self.begin_date = str(begin_date)
        self.end_date = str(end_date)
        

    def __str__(self):
        return f'{self.name},' \
            f'{self.facility_type.value},' \
            f'{self.location},' \
            f'{self.begin_date},' \
            f'{self.end_date},'

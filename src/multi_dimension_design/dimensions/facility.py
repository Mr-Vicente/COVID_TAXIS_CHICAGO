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
class Facility:
    """Representing the location region dimension in multimodal design"""
    id: int
    name: str
    type: FACILITY
    location: Location
    begin_date: Date
    end_date: Date


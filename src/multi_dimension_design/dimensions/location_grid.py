#############################
#   Imports and Contants    #
#############################

# Python modules
from dataclasses import dataclass

# Local module

@dataclass
class Location_Grid:
    """Representing the location region dimension in multimodal design"""
    key: int
    latitude_region: float
    longitude_region: float
    zip_code: int


#############################
#   Imports and Contants    #
#############################

# Python modules
from dataclasses import dataclass

# Local module

@dataclass
class Location:
    """Representing the location region dimension in multimodal design"""
    key: int
    latitude: float
    longitude: float
    zip_id: int
    zip_code: int
    zip_geometry: list
    zip_shape_area: float


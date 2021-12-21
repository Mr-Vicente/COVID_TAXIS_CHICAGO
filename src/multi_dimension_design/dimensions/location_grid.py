#############################
#   Imports and Contants    #
#############################

PRECISION = 6

# Python modules

# Remote modules
from shapely.geometry import Point
from shapely.wkt import loads

# Local module

class Location_Grid:
    """Representing the location region dimension in multimodal design"""
    original_key: int
    latitude: float
    longitude: float
    zip_code: int
    zip_geometry: list
    zip_shape_area: float

    def __init__(self, original_key, location, zip_info):
        self.original_key = original_key
        self.latitude = self.get_lower_precision(float(location[0]))
        self.longitude = self.get_lower_precision(float(location[1]))
        self.zip_code = zip_info[2]
        self.zip_shape_area = zip_info[3]
        #self.zip_geometry = zip_info[0]

    def get_lower_precision(self, coord_unit):
        return round(coord_unit, PRECISION)

    @classmethod
    def extract_zip_info(cls, zip_codes, location):
        point = Point(float(location[0]), float(location[1]))
        print(point)
        for zip_info in zip_codes:
            polygon = zip_info[0]
            if polygon.contains(point):
                return zip_info
        return ""
    @classmethod
    def poligon_str_2_poligon(cls, poligon_str):
        poligon = loads(poligon_str)
        return poligon

    def __str__(self):
        return f'{self.latitude},' \
               f'{self.longitude},' \
               f'{self.zip_code},' \
               f'{self.zip_shape_area}' #\
               #f'{self.zip_geometry}'


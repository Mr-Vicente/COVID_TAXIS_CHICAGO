#############################
#   Imports and Contants    #
#############################

# Python modules

# Remote modules
from shapely.geometry import Point
from shapely.wkt import loads

# Local module

class Location:
    """Representing the location region dimension in multimodal design"""
    original_key: int
    latitude: float
    longitude: float
    zip_id: int
    zip_code: int
    zip_geometry: list
    zip_shape_area: float

    def __init__(self, original_key, location, zip_info):
        self.original_key = original_key
        self.latitude = location[0]
        self.longitude = location[1]
        self.zip_id = zip_info[1]
        self.zip_code = zip_info[2]
        self.zip_shape_area = zip_info[3]
        self.zip_geometry = zip_info[0]

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
               f'{self.zip_id},' \
               f'{self.zip_code},' \
               f'{self.zip_shape_area},' \
               f'{self.zip_geometry}'







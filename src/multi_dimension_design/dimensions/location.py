#############################
#   Imports and Contants    #
#############################

# Python modules

# Remote modules
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.wkt import dumps, loads

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
        print(zip_info)
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

    @classmethod
    def poligon_str_2_poligon_2(cls, poligon_vec):
        #poligon_vec = poligon_str.split(',')
        poligon_vec[0] = poligon_vec[0].split('(((')[-1]
        poligon_vec[-1] = poligon_vec[-1].split(')))')[0]
        poligon_vec = [p.strip() for p in poligon_vec]
        poligon_temp = []
        for p in poligon_vec:
            p = p.split(' ')
            p[0] = p[0].replace('(', '')
            p[-1] = p[-1].replace(')', '')
            p = (float(p[0]), float(p[-1]))
            poligon_temp.append(p)
        poligon = Polygon(poligon_temp)
        return poligon

    def __str__(self):
        return f'{self.latitude},' \
               f'{self.longitude},' \
               f'{self.zip_id},' \
               f'{self.zip_code},' \
               f'{self.zip_shape_area},' \
               f'{self.zip_geometry}'







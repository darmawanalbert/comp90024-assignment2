# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.au


import os
from shapely.geometry import Point, MultiPolygon
from shapely.geometry.polygon import Polygon
import sys
import json
# sys.path.append('../')

# GEOJSON_ADDRESS='../frontend/components/cities_top50_simplified.geojson'
GEOJSON_ADDRESS = os.environ.get('GEOJSON_ADDRESS') if os.environ.get('GEOJSON_ADDRESS') != None else "cities_top50_simplified.geojson" 
current_path = os.path.dirname(__file__)
new_path = os.path.relpath(GEOJSON_ADDRESS,current_path)

class LocationUtils():
    def __init__(self):
        try:
            self.location_grid = []
            with open(GEOJSON_ADDRESS,'r') as f:
                self.geo_location = json.load(f)
            for i in range(len(self.geo_location['features'])):
                self.location_dict = {}
                self.location_dict['location_id'] = self.geo_location['features'][i]['properties']['UCL_CODE_2016']
                self.location_dict['location_name'] = self.geo_location['features'][i]['properties']['UCL_NAME_2016']
                self.location_dict['type'] = self.geo_location['features'][i]['geometry']['type']
                self.location_dict['coordinates_polygon'] = self.geo_location['features'][i]['geometry']['coordinates']

                self.location_grid.append(self.location_dict)
        except Exception as e:
            print(e)
    
    def search_grid(self,tweet_location):
        if len(tweet_location) >2:
            self.points = Polygon(tweet_location)
        else:
            self.points = Point(tweet_location)
            
        self.location_found = False

        for location in self.location_grid:
            if location['type'] == 'Polygon':
                self.container_box = Polygon(location['coordinates_polygon'][0])
                if self.container_box.within(self.points):
                    self.location_found = True
                    return self.location_found
            elif location['type'] == 'MultiPolygon':
                for polygon in location['coordinates_polygon']:
                    self.container_box = Polygon(polygon[0])
                    if self.container_box.within(self.points):
                        self.location_found = True
                        return self.location_found
        return self.location_found
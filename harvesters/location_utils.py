#COMP90024 Team 1
#Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
##Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
#I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
#Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
#Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au


import os
from shapely.geometry import Point, MultiPolygon
from shapely.geometry.polygon import Polygon
import sys
import json
sys.path.append('../')

GEOJSON_ADDRESS='../frontend/components/cities_top50_simplified.geojson'
current_path = os.path.dirname(__file__)
new_path = os.path.relpath(GEOJSON_ADDRESS,current_path)

class LocationUtils():
    def __init__(self):
        try:
            self.location_grid = []
            with open(new_path,'r') as f:
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
        self.location_id = None
        self.location_name = None

        for location in self.location_grid:
            if location['type'] == 'Polygon':
                self.container_box = Polygon(location['coordinates_polygon'][0])
                if self.container_box.contains(self.points):
                    self.location_found = True
                    self.location_id = location['location_id']
                    self.location_name = location['location_name']
                    return self.location_found, self.location_id,self.location_name
            elif location['type'] == 'MultiPolygon':
                for polygon in location['coordinates_polygon']:
                    self.container_box = Polygon(polygon[0])
                    if self.container_box.within(self.points):
                        print('yes')
                        self.location_found = True
                        self.location_id = location['location_id']
                        self.location_name = location['location_name']
                        return self.location_found, self.location_id,self.location_name
        return self.location_found, self.location_id, self.location_name

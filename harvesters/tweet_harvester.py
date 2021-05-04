import sys
sys.path.append('../')

import tweepy
import json 
import pandas as pd
from database.db_utils import DB_Utils
from urllib3.exceptions import ProtocolError
import os
from shapely.geometry import Point, MultiPolygon
from shapely.geometry.polygon import Polygon


LOCATION = [144.5552,-38.1207,145.5494,-37.5803]
VIC = [139.19,-38.72,149.7,-34.14]
AUS = [113.62,-44.1,153.14,-10.75]

GEOJSON_ADDRESS='../frontend/components/cities_top50_simplified.geojson'
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') != None else "comp90024_tweet_harvest" 
API_TOKENS = os.environ.get('API_TOKENS') if os.environ.get('API_TOKENS') != None else "twitter-api-tokens.csv" 

creds_file = pd.read_csv(API_TOKENS,encoding='utf-8',sep=';')

#Gotta iterate through this later to fully utilize all our keys 
consumer_api_key = creds_file['API_KEY'][0]
consumer_secret_key = creds_file['API_SECRET_KEY'][0]
consumer_access_token = creds_file['ACCESS_TOKEN'][0]
consumer_token_secret = creds_file['ACCESS_TOKEN_SECRET'][0]

#authentication object
auth = tweepy.OAuthHandler(consumer_api_key,consumer_secret_key)

#Set access token and access token secret
auth.set_access_token(consumer_access_token,consumer_token_secret)

#API Object
api = tweepy.API(auth, wait_on_rate_limit=True)

db_conn =DB_Utils()
db_conn.db_connect(DB_NAME)

#Load GeoJSON locations
current_path = os.path.dirname(__file__)
new_path = os.path.relpath(GEOJSON_ADDRESS,current_path)

#A function to load the GeoJson file of cities
def load_geojson(file_path):
    location_details = []
    with open(file_path,'r') as f:
        geo_location = json.load(f)
    
    for i in range(len(geo_location['features'])):
        location_dict = {}
        location_dict['location_id'] = geo_location['features'][i]['properties']['UCL_CODE_2016']
        location_dict['location_name'] = geo_location['features'][i]['properties']['UCL_NAME_2016']
        location_dict['type'] = geo_location['features'][i]['geometry']['type']
        location_dict['coordinates_polygon'] = geo_location['features'][i]['geometry']['coordinates']

        location_details.append(location_dict)

    return location_details

list_location = load_geojson(new_path)

#A function to check if a tweet is within the listed 50 cities
def search_location(tweet_location, location_grid):
    points = Polygon(tweet_location)
    
    location_found = False

    for location in location_grid:
        if location['type'] == 'Polygon':
            container_box = Polygon(location['coordinates_polygon'][0])
            if container_box.within(points):
                location_found = True
                return location_found
        elif location['type'] == 'MultiPolygon':
            for polygon in location['coordinates_polygon']:
                container_box = Polygon(polygon[0])
                if container_box.within(points):
                    location_found = True
                    return location_found
    return location_found

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self,status):
        print(status.text)
    
    def on_data(self, data):
        try:      
            tweet_data = json.loads(data)
            loc = tweet_data["place"]['bounding_box']['coordinates'][0]
            gridsearch = search_location(loc,list_location)
            if gridsearch == True:
                #tweet_id = tweet_data['id_str']
                tweet_data['_id'] = tweet_data.pop('id_str')
                
                print(tweet_data)
                #print(tweet_data['place']['full_name'])
                db_conn.save(DB_NAME,tweet_data)  
        except BaseException as e:
            print("Error on data: %s" % str(e))
       
    def on_error(self,status):
        print(status)
    
    def on_exception(self,exception):
        print(exception)
        return

stream_listener = CustomStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

while True:
    try:
        stream.filter(locations =AUS,languages=['en'])
    
    except ConnectionRefusedError:
        print("Error: stream connection failed")
        continue
    except FileNotFoundError as e:
        print(e)
        exit(-1)
    except tweepy.RateLimitError:
        print("Hit Twitter API Rate limit")
        #Sleep for 20 mins
        time.sleep(20*60)
        continue
    except Exception as e:
        print(e)
        continue
# COMP90024 Team 1
# Albert Darmawan (1168452) - darmawana@student.unimelb.edu.au
# Clarisca Lawrencia (1152594) - clawrencia@student.unimelb.edu.au
# I Gede Wibawa Cakramurti (1047538) - icakramurti@student.unimelb.edu.au
# Nuvi Anggaresti (830683) - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah Putra (1191132) - wildananugra@student.unimelb.edu.auS

import sys
sys.path.append('../')

import tweepy
import json 
import pandas as pd
from location_utils import LocationUtils
from database.db_utils import DB_Utils
import os
import time


#Defining constants
AUS = [113.62,-44.1,153.14,-10.75]
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') != None else "test_new1" 
API_TOKENS = os.environ.get('API_TOKENS') if os.environ.get('API_TOKENS') != None else "twitter-api-tokens.csv" 

#Getting Credentials for Twitter API
creds_file = pd.read_csv(API_TOKENS,encoding='utf-8',sep=';')
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

#CouchDB Database Object 
db_conn =DB_Utils()
db_conn.db_connect(DB_NAME)


#Location Object
location_geojson = LocationUtils()


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self,status):
        print(status.text)
    
    def on_data(self, data):
        try:      
            tweet_data = json.loads(data)
            loc = tweet_data["place"]['bounding_box']['coordinates'][0]

            gridsearch = location_geojson.search_grid(loc)
            if gridsearch[0] == True:
                #tweet_id = tweet_data['id_str']
                tweet_data['_id'] = tweet_data.pop('id_str')
                tweet_data['place']['AURIN_id'] = gridsearch[1]
                tweet_data['place']['AURIN_loc_name'] = gridsearch[2]
               # print(tweet_data)
                #print(tweet_data['place']['full_name'])
                db_conn.save(DB_NAME,tweet_data)  
        except BaseException as e:
            print("Error on data: %s" % str(e))
       
    def on_error(self,status):
        print(status)
        if status =='420':
            time.sleep(20*60)
    
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
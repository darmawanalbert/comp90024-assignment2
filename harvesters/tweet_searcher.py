# COMP90024 Team 1
# Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
# Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
# I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
# Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au

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
AUS_LONG_LAT ='25.2744,133.7751,50km'
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') != None else "comp90024_tweet_harvest" 
API_TOKENS = os.environ.get('API_TOKENS') if os.environ.get('API_TOKENS') != None else "twitter-api-tokens.csv" 

#Getting Credentials for Twitter API
creds_file = pd.read_csv(API_TOKENS,encoding='utf-8',sep=';')
consumer_api_key = creds_file['API_KEY'][1]
consumer_secret_key = creds_file['API_SECRET_KEY'][1]
consumer_access_token = creds_file['ACCESS_TOKEN'][1]
consumer_token_secret = creds_file['ACCESS_TOKEN_SECRET'][1]

#authentication object
auth = tweepy.OAuthHandler(consumer_api_key,consumer_secret_key)

#Set access token and access token secret
auth.set_access_token(consumer_access_token,consumer_token_secret)

#API Object
api = tweepy.API(auth, wait_on_rate_limit=True,parser=tweepy.parsers.JSONParser())

#CouchDB Database Object 
db_conn =DB_Utils()
db_conn.db_connect(DB_NAME)

#Location Object
location_geojson = LocationUtils()

max_counter=100
while True:
    try:
        for i in range(max_counter):
         
            tweetlist = api.search(geocode=AUS_LONG_LAT,count=100,lang=['en'])
            statuses = tweetlist['statuses']
            for tweet_data in statuses:
               
                if tweet_data['coordinates']!=None:
                    loc = tweet_data["coordinates"]
                    print(tweet_data)
                    gridsearch = location_geojson.search_grid(loc)
                    if gridsearch == True:
                        tweet_data['_id'] = tweet_data.pop('id_str')      
                        print(tweet)
                        db_conn.save(DB_NAME,tweet_data)  
  
    except tweepy.RateLimitError:
        print('Rate Limit Encountered. Going to sleep')
        time.sleep(20*60)
    except Exception as e:
        print(e)
    time.sleep(20*60)

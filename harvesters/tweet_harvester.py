import sys
sys.path.append('../')

import tweepy
import json 
import pandas as pd
from database.db_utils import DB_Utils
from urllib3.exceptions import ProtocolError

LOCATION = [144.5552,-38.1207,145.5494,-37.5803]
VIC = [139.19,-38.72,149.7,-34.14]
AUS = [113.62,-44.1,153.14,-10.75]

DB_NAME = 'twitter_db_test'

creds_file = pd.read_csv('twitter-api-tokens.csv',encoding='utf-8',sep=';')

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

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self,status):
        print(status.text)
    
    def on_data(self, data):
        try:      
            tweet_data = json.loads(data)
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
        stream.filter(locations = AUS,languages=['en'])
    
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
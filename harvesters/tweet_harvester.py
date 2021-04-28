import tweepy
import json 
import pandas as pd
import couchdb
from urllib3.exceptions import ProtocolError

LOCATION = [144.5552,-38.1207,145.5494,-37.5803]
VIC = [139.19,-38.72,149.7,-34.14]
AUS = [113.62,-44.1,153.14,-10.75]
ADDRESS='http://admin:admin@115.146.95.84:15984/'
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

def connection_to_db():
    try:
        server = couchdb.Server(ADDRESS)
        #server.resource.credentials = (USERNAME,PASSWORD)
        print('Connected to server')
    except Exception as e:
        print('Server not found')

    try:
        db = server[DB_NAME]
        print('db found')
    except Exception as e:
        print(e)
        print('NO DB FOUND')
        exit(-1)
    return db

db_conn = connection_to_db()

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self,status):
        print(status.text)
    
    def on_data(self, data):
        try:
            # with open('tweets_collected.json', 'a', encoding='utf-8') as fp:
            #    # fp.write('\t')
            #     print(data)
            #     fp.write(data)
            #     print('Written')       
            tweet_data = json.loads(data)
            db_conn.save(tweet_data)  
            print("Written in DB")
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
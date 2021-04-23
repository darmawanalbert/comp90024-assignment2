import tweepy
import json 
import pandas as pd

LOCATION = [144.5552,-38.1207,145.5494,-37.5803]
VIC = [139.19,-38.72,149.7,-34.14]
AUS = [113.62,-44.1,153.14,-10.75]

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
api = tweepy.API(auth)

#Temporary loading of json file instead of couchdb
#def load_json(file_path):



class CustomStreamListener(tweepy.StreamListener):
    def on_status(self,status):
        print(status.text)
    
    def on_data(self, data):
        
        tweet = json.loads(data)
        tweet_id= tweet['id_str']
        tweet_date = tweet['created_at']
        tweet_text = tweet['text']
        tweet_city = tweet['place']['full_name']
        tweet_loc = tweet['place']['bounding_box']['coordinates']

        tweet_dict= {'id_str':tweet_id, 'created_at': tweet_date, 'text':tweet_text,'city_name':tweet_city,'coordinates':tweet_loc}
        
        tweet_str = str(tweet_dict)+"\n"
        
        #Temporarily store all the harvested tweet in a json file 
        try:
            with open('tweets_collected.json', 'a', encoding='utf-8') as fp:
                fp.write(tweet_str)
          
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

    #Rate Limit Exception 
    except tweepy.RateLimitError:
        print("Hit Twitter API Rate limit")
        for i in range(3, 0, -1):
            print("Wait for {} mins.".format(i * 5))
            time.sleep(5 * 60)
    
    except Exception as e:
        print(e)
        continue
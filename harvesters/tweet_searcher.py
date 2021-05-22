# COMP90024 Team 1
# Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
# Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
# I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
# Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au

import sys
sys.path.append('../')
import couchdb
import csv
import tweepy
import json 
import pandas as pd
from location_utils import LocationUtils
import os
import time

#Defining constants
CITYFILE = 'city_details.csv'
ADDRESS= os.environ.get('ADDRESS') if os.environ.get('ADDRESS') != None else "http://admin:admin@45.113.235.136:15984/"
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') != None else "comp90024_tweet_search" 
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
server = couchdb.Server(ADDRESS)
db_conn = server[DB_NAME]

#Location Object
location_geojson = LocationUtils()

#A function the coordinates of the 8 capital cities
def load_coordinates(filepath):
    coordinates=list()
    with open(filepath, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for rows in reader: 
            coordinates.append(rows)
    return coordinates

#A function to save the tweet
def save_tweet(tweet_data,location):
    #Search if the tweet is within the top 50 cities grid
    gridsearch = location_geojson.search_grid(location)
    if gridsearch[0] == True:
        #Change the _id to id_str of the tweet to avoid duplication in db
        #Add aurin location ID and aurin location name
        tweet_data['_id'] = tweet_data.pop('id_str')
        tweet_data['AURIN_id'] = gridsearch[1]
        tweet_data['AURIN_loc_name'] = gridsearch[2]    
        db_conn.save(tweet_data)  

#A function to initiate tweet search api 
def search_tweet(location,maxId):

    location_details = [float(location[2]),float(location[1])]
    join_coor = ','.join(location[1:])
    try:
        #The max ID helps in the searcher to find tweets until the maximum tweet ID 
        #the longer the tweet ID indicates that the tweet is most recent
        #Hence it will prompt the search APi to search for older tweets
        if maxId != '':
            tweetlist = api.search(geocode=join_coor,count=100,lang=['en'],max_id = maxId)
        else:
            tweetlist = api.search(geocode=join_coor,count=100,lang=['en'])
        statuses = tweetlist['statuses']
        for tweet_data in statuses:
            save_tweet(tweet_data,location_details)
            print('Saved Successfully')
    #Force sleep the searcher when it reaches limit
    #It will start again after 20 mins
    except tweepy.RateLimitError:
        print('Rate Limit Encountered. Going to sleep')
        time.sleep(20*60)
    except Exception as e:
        print(e)
    return tweetlist['search_metadata']['max_id']

def main():
    capital_cities = load_coordinates(CITYFILE)
    maxId=''
    
    while True:
        #Iterating through all the capital cities
        for city in capital_cities:
            try:
                #Load the most current maxID
                with open('curr_maxID.txt', mode='r', encoding='utf-8-sig') as file:
                    for row in file:
                        maxId = row
                file.close()

                new_maxid = search_tweet(city,maxId)

                #Write the latest maxID into the file
                file2 = open('curr_maxID.txt', 'w')
                file2.write(str(new_maxid))
                file2.close()
            except: 
                pass
main()
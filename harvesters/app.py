# COMP90024 Team 1
# Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
# Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
# I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
# Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au

from requests_oauthlib import OAuth1Session
import requests
from datetime import datetime
import urllib
import os
import uuid
import json

TWEET_USER = os.environ.get('QUERY') if os.environ.get('QUERY') != None else "australia"
DB_HOST = os.environ.get('DBHOST') if os.environ.get('DBHOST') != None else "http://admin:admin@127.0.0.1:5984/"
DB_NAME = os.environ.get('DBNAME') if os.environ.get('DBNAME') != None else "testdb"

def twitter_key():
    return {
        "consumer_key":"miqzA0lkGA90VdybfkKXXAjaX",
        "consumer_secret": "IQ3Na3k0NwrYbCHJlqZPDBTj0jWpadZvpF2ti1F6cT3IGAXEO2",
        "access_token":"2326421154-2c1k5Qq5bvGZsezoihZZEVWPxBNIa67GJDTBl4N",
        "access_token_secret":"QsES893a58omKIHwiL9JP2fpeS0g5OLJMKLIhfjBD6tUf"
    }

key = twitter_key()
twitter = OAuth1Session(key['consumer_key'], client_secret=key['consumer_secret'], resource_owner_key=key['access_token'], resource_owner_secret=key['access_token_secret'])
q = urllib.parse.urlencode({'q':TWEET_USER,'count': 100, 'tweet_mode':'extended'})
url = f'https://api.twitter.com/1.1/search/tweets.json?{q}'
response = twitter.get(url)
tweets = []
if(response.status_code == 200):
    response_json = response.json()
    for status in response_json['statuses']:
        tweets.append({
            'posted_at': status["created_at"],
            'tweet_id': status['id_str'],
            'text' : status['full_text'].replace("\'",""),
            'tweet_link': f"https://www.twitter.com/{status['user']['screen_name']}/status/{status['id_str']}",
            'author_screen_name': status['user']['screen_name'],
            'author_protected': status['user']['protected'],
            'author_followers_count': status['user']['followers_count'],
            'author_statuses_count': status['user']['statuses_count'],
            'author_verified': status['user']['verified']
        })
else:
    print(response.json())

for tweet in tweets:
    try:
        url = f"{DB_HOST}{DB_NAME}"
        query = {"selector": {"tweet_id": {"$eq": tweet['tweet_id']}}}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{url}/_find",headers=headers,data=json.dumps(query))
        response_json = json.loads(response.text)
        if(len(response_json['docs']) == 0):
            response = requests.put(f"{url}/{uuid.uuid4()}", data=json.dumps(tweet))
            print(response.text)
        else:
            print(f"tweetid: {tweet['tweet_id']} exists")
    except Exception as err:
        print(f"ERROR {err}")

print("done.")
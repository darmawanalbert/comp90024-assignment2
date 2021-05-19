import requests
import json
import pandas as pd

#url = "http://admin:admin@45.113.235.136:15984/comp90024_tweet_harvest/_design/topic_modelling/_view/count_by_place"
# url = "http://admin:admin@45.113.235.136:15984/comp90024_tweet_harvest/_design/topic_modelling/_view/by_date"
url = "http://admin:admin@45.113.235.136:15984/comp90024_tweet_harvest/_design/topic_modelling/_view/by_date_and_place"
#obj = {"startkey": [[2021, 5, 9]], "endkey": [[2021, 5, 9], {}]}
obj = {"key": [[2021, 5, 9],'Melbourne']}
# obj = {"startkey": [[2021, 5, 9]], "endkey": [[2021, 5, 9], {}]}

data = json.dumps(obj).encode('utf-8')

headers = {"content-type": "application/json"}

count_data = requests.post(url, data=data, headers=headers)
count_json = count_data.text
count_dict = json.loads(count_json)

# print(count_data.text)

tweets_df = pd.DataFrame()
for i in count_dict['rows']:
    
    tweet_id = str(i['value']['id'])
    tweet = i['value']['text']
    date = i['key'][0]
    location_tweet = i['key'][1]

    tweet_data=dict(id=tweet_id, text=tweet,location=location_tweet, date_created=date)
    tweets_df = tweets_df.append(tweet_data,ignore_index= True)

print(tweets_df)

# DB sample requests for future reference

import requests
import json

headers = {"content-type": "application/json"}

# This is for finding the count filtered by date
url = "http://admin:admin@45.113.235.136:15984/comp90024_tweet_harvest/_design/topic_modelling/_view/count_by_place"

obj = {"startkey": [[2021, 5, 9]], "endkey": [[2021, 5, 9], {}], "group": True}
data = json.dumps(obj).encode('utf-8')

count_data = requests.post(url, data=data, headers=headers)
count_json = count_data.text
count_dict = json.loads(count_json)

# This is for finding the single key by date
url = "http://admin:admin@45.113.235.136:15984/comp90024_tweet_harvest/_design/topic_modelling/_view/by_date"

obj = {"key": [2021, 5, 9]}
data = json.dumps(obj).encode('utf-8')

date_data = requests.post(url, data=data, headers=headers)
date_json = date_data.text
date_dict = json.loads(date_json)

# This is for finding data just filtered by date but in by_date_and_place
url = "http://admin:admin@45.113.235.136:15984/comp90024_tweet_harvest/_design/topic_modelling/_view/by_date_and_place"

obj = {"startkey": [[2021, 5, 9]], "endkey": [[2021, 5, 9], {}]}
data = json.dumps(obj).encode('utf-8')

only_date_data = requests.post(url, data=data, headers=headers)
only_date_json = only_date_data.text
only_date_dict = json.loads(only_date_json)

# This is for finding data just filtered by date but in by_date_and_place
url = "http://admin:admin@45.113.235.136:15984/comp90024_tweet_harvest/_design/topic_modelling/_view/by_date_and_place"

obj = {"key": [[2021, 5, 9], "Melbourne"]}
data = json.dumps(obj).encode('utf-8')

date_place_data = requests.post(url, data=data, headers=headers)
date_place_data = date_place_data.text
date_place_dict = json.loads(date_place_data)
# COMP90024 Team 1
# Albert, Darmawan (1168452) - Jakarta, ID - darmawana@student.unimelb.edu.au
# Clarisca, Lawrencia (1152594) - Melbourne, AU - clawrencia@student.unimelb.edu.au
# I Gede Wibawa, Cakramurti (1047538) - Melbourne, AU - icakramurti@student.unimelb.edu.au
# Nuvi, Anggaresti (830683) - Melbourne, AU - nanggaresti@student.unimelb.edu.au
# Wildan Anugrah, Putra (1191132) - Jakarta, ID - wildananugra@student.unimelb.edu.au

# Installing the necessary packages for Machine Learning Modelling
import couchdb
import requests
import nltk
import json
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import re
import gensim
from nltk.stem import WordNetLemmatizer
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
import os
import hashlib
from datetime import datetime, timedelta


#Download required nltk  files
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

#Creating DB Connection
DB_NAME = os.environ.get('DB_NAME') if os.environ.get('DB_NAME') != None else "comp90024_lda_scoring" 
ADDRESS = os.environ.get('ADDRESS') if os.environ.get('ADDRESS') != None else "http://admin:admin@45.113.235.136:15984"

print(DB_NAME)
print(ADDRESS)

server = couchdb.Server(ADDRESS)
db_conn = server[DB_NAME]

#Defining the view object
# db_views_stream = "http://admin:admin@45.113.235.136:15984/comp90024_tweet_harvest/_design/topic_modelling/_view/by_date_and_place"
# db_views_search = "http://admin:admin@45.113.235.136:15984/comp90024_tweet_search/_design/topic_modelling/_view/by_date_and_place"

db_views_stream = f"{ADDRESS}/comp90024_tweet_harvest/_design/topic_modelling/_view/by_date_and_place"
db_views_search = f"{ADDRESS}/comp90024_tweet_search/_design/topic_modelling/_view/by_date_and_place"

#top 50 cities file path
GEOJSON_ADDRESS = os.environ.get('GEOJSON_ADDRESS') if os.environ.get('GEOJSON_ADDRESS') != None else "cities_top50_simplified.geojson" 
current_path = os.path.dirname(__file__)
new_path = os.path.relpath(GEOJSON_ADDRESS,current_path)

#Defining the file path of the subject corpus
POLITICS_FILE='politics.txt'
SPORTS_FILE ='sports.txt'
PLACES_FILE ='places.txt'
ENTERTAINMENT_FILE = 'entertainment.txt'
EDUCATION_FILE= 'education.txt'
BUSINESS_FILE = 'business.txt'

#Get yesterday's date to obtain data from view
date_yesterday=datetime.today() - timedelta(1)
date_yesterday= datetime.strftime(date_yesterday,'%Y,%m,%d')
date_list = list(map(int, date_yesterday.split(',')))

#A function to load the top 50 cities' names
def load_top50_cities(file_name):
    try:
        city_names = []
        with open(file_name,'r') as f:
            geo_location = json.load(f)
        for i in range(len(geo_location['features'])):
            city_name = geo_location['features'][i]['properties']['UCL_NAME_2016']
            city_names.append(city_name.lower())
    except Exception as e:
            print(e)
    return city_names

# A function to load the subject corpus
def load_txt(file_name):
    list_word=[]
    try:
        with open(file_name) as phrases:
            for word in phrases:
                word = word.lower()
                word = re.sub(r'[^\w\s]','',word)
                word = word.strip()
                word = word.split()
                i=0
                temp_word=''
                while i < len(word):
                    temp_word = temp_word+" "+word[i]
                    temp_word = temp_word.lstrip()
                    i+=1
                list_word.append(temp_word)
    except Exception as e:
        print(e)
    return list_word

# A function to extract the lenght of the longest word in the corpus
def longest_word(filename):
    max_word = max(open(filename), key=len)
    len_max_word = len(max_word.split())
    
    return len_max_word

# A function to obtain the score for each subject
def get_score(list_of_words,tweet_text,maxlen):
    counter=0
    for tokens in tweet_text:
        max_loop = maxlen
        while max_loop >=0:
            index=0
            while index < len(tokens)-max_loop:
                temp=''
                j=0
                while j<=max_loop:
                    temp+=tokens[j+index]+' '
                    j+=1
                temp = temp.rstrip()
                if temp in list_of_words:
                    counter+=1
                    index+=1
                else:
                    index+=1
            max_loop-=1
    return counter

# A function to retrieve data from the database
def get_data_db(url,views):
    data = json.dumps(views).encode('utf-8')

    headers = {"content-type": "application/json"}

    req_data = requests.post(url, data=data, headers=headers)
    json_string= req_data.text
    load_dict = json.loads(json_string)

    tweets_df = pd.DataFrame()
    for i in load_dict['rows']:
    
        tweet_id = str(i['value']['id'])
        tweet = i['value']['text']
        date = i['key'][0]
        location_tweet = i['key'][1]

        tweet_data=dict(id=tweet_id, text=tweet,location=location_tweet, date_created=date)
        tweets_df = tweets_df.append(tweet_data,ignore_index= True)
    return tweets_df

#A function to tokenize the text in the tweets
#text (args): Takes in a list of string 
def tokenize_text(text):    
    #Assigning the stop words for preprocessing 
    #Add punctuations as a part of stop words
    stop_words = stopwords.words('english')
    stop_words += list(string.punctuation)
    tokens = word_tokenize(text)
    tokens_stopwords_none = [t.lower() for t in tokens if t.lower() not in stop_words]
    return tokens_stopwords_none

# A function to fix the encoding 
def fix_encode(text):
    text = text.replace(r'&amp;',r'and')
    text = text.replace(r'&lt;',r'<')
    text = text.replace(r'&gt;',r'>')
    text = text.encode('ascii','ignore')
    encoded_text = text.decode()

    return encoded_text

#A function to remove punctuation values in the tweeta
#text (args): Takes in a list of string 
def remove_punctuations(text):
    text = text.translate(str.maketrans('', '',string.punctuation))
    return text

#A function that lemmatizes each word in the text document
def lemmatize_text(text):
    #A lemmatizer constant to lemmatize text within a tweet
    lemmatizer = WordNetLemmatizer()
    lemmatized=[]
    for word in text:
        lemmatized.append(lemmatizer.lemmatize(word))
    return lemmatized

#Extracting keywords by using LDA algorithm 
def lda_topics(text):
    text_dict = Dictionary(text)
    text_bagofwords = [text_dict.doc2bow(tweet) for tweet in text]
    k=5
    tweets_lda = LdaModel(text_bagofwords,
                        num_topics = k,
                        id2word = text_dict,
                        random_state =1,
                        passes=2)

    ##Converting from tuuple to dictionary
    tuple_topics = tweets_lda.show_topics()
    topics_dict=dict()
    for i in range(0, tweets_lda.num_topics):
        for token, score in tweets_lda.show_topic(i):
            topics_dict[token] = str(score)

    return tuple_topics, topics_dict

def hash_id(uniqueid):
    uniqueid = remove_punctuations(uniqueid)
    uniqueid = "".join(uniqueid.split())
    encode_str = uniqueid.encode('utf-8')
    hash_lda = hashlib.md5()
    hash_lda.update(encode_str)

    return hash_lda.hexdigest()

def main():

    #Load Corpus
    education = load_txt(EDUCATION_FILE)
    entertainment = load_txt(ENTERTAINMENT_FILE)
    places = load_txt(PLACES_FILE)
    sports = load_txt(SPORTS_FILE)
    politics = load_txt(POLITICS_FILE)
    business= load_txt(BUSINESS_FILE)

    #Finding max word in corpus
    business_max_word = longest_word(BUSINESS_FILE)
    sports_max_word = longest_word(SPORTS_FILE)
    politics_max_word = longest_word(POLITICS_FILE)
    education_max_word  = longest_word(EDUCATION_FILE)
    places_max_word  = longest_word(PLACES_FILE)
    entertainment_max_word  = longest_word(ENTERTAINMENT_FILE)

    #Load the top 50 cities name 
    #Iterate through the list to obtain views for each 50 cities
    list_city = load_top50_cities(new_path)
    for i in range(len(list_city)):

        #Using yesterday's date to query harvested data 
        obj = {"key": [date_list, list_city[i]]}
    
        #Obtaining data from db
        tweets_stream = get_data_db(db_views_stream,obj)
        tweets_search = get_data_db(db_views_search,obj)

        classifier_id = "clf"+str(obj['key'][1])+date_yesterday
        classifier_id = hash_id(classifier_id)
        
        #Combine data from search and stream
        tweets_data = pd.concat([tweets_stream,tweets_search],ignore_index=True,sort=False)
        tweets_count = len(tweets_data.index)
        
        if not tweets_data.empty:      
            #Pre-processing of tweet file
            #Drop duplicated tweet id
            tweets_data.drop_duplicates(subset ="id",
                     keep = 'first', inplace = True)
            tweet_text= tweets_data['text'].str.replace(r"http\S+","")
            tweet_text = tweet_text.apply(fix_encode)
            tweet_text = tweet_text.apply(remove_punctuations)
            tweet_text = tweet_text.apply(tokenize_text)
            tweet_text = tweet_text.apply(lemmatize_text)

            #Obtain topic keywords using LDA
            lda_res = lda_topics(tweet_text)

            #Obtain the score for each subject category
            sports_score = get_score(sports,tweet_text,sports_max_word)
            places_score = get_score(places,tweet_text, places_max_word)
            politics_score = get_score(politics,tweet_text, politics_max_word)
            education_score = get_score(education,tweet_text, education_max_word)
            entertainment_score = get_score(entertainment,tweet_text, entertainment_max_word)
            business_score = get_score(business, tweet_text, business_max_word)
            
            #Convert to dictionary file 
            data_record =dict(_id = str(classifier_id),date =date_yesterday, location=str(obj['key'][1]),
                            total_tweets = str(tweets_count),
                            lda_result = lda_res[1], score_sports = str(sports_score),
                            score_places = str(places_score), score_politics= str(politics_score),
                            score_education = str(education_score), score_entertainment=str(entertainment_score),
                            score_business=str(business_score))
            try:  
                db_conn.save(data_record)  
                print('Successfully recorded classifier data')
            except Exception as e:
                print(e)
main() 
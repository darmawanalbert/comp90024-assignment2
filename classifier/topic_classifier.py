# Installing the necessary packages for Machine Learning Modelling

import ijson
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import re
from wikiapi import WikiApi
import gensim
from nltk.stem import WordNetLemmatizer
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel

LOCATION_CITY = 'melbourne'
file_path ='smallTwitter.json'

#Assigning the stop words for preprocessing 
#Add punctuations as a part of stop words
stop_words = stopwords.words('english')
stop_words += list(string.punctuation)

#A lemmatizer constant to lemmatize text within a tweet
lemmatizer = WordNetLemmatizer()

#def connect_db

#A function to load the json file
def load_json(tweet_file):
    tweets = pd.DataFrame()
    with open(tweet_file, 'r', encoding='utf-8') as f:
        #Genks ini masih ikutin si small twitter nanti ini diganti sesuai dengan couch db
        objects = ijson.items(f, 'rows.item')
        for line in objects:
            if line['value']['properties']['location']== LOCATION_CITY:
                #if  tweet_date = line['value']['properties']['created_at'] between which ever date assigned
                tweet_id = line['id']
                twt_text = line['value']['properties']['text']
                twt_loc = line['value']['properties']['location']
                twt_data = dict(id=tweet_id,location=twt_loc, text=twt_text)
                tweets = tweets.append(twt_data,ignore_index=True)
    return tweets
#A function to tokenize the text in the tweets
#text (args): Takes in a list of string 
def tokenize_text(text):
    tokens = word_tokenize(text)
    tokens_stopwords_none = [t.lower() for t in tokens if t.lower() not in stop_words]
    return tokens_stopwords_none

#A function to remove numeric values in the tweeta
#text (args): Takes in a list of string 
def remove_numbers(text):
    removed_numbers = list(filter(lambda x: x.isalpha(), text))
    return removed_numbers


def lemmatize_text(text):
    lemmatized=[]
    for word in text:
        lemmatized.append(lemmatizer.lemmatize(word))
    return lemmatized

def get_relevant_articles(keywords, search_depth=5, keyword_summary=5):
    
    if len(keywords)==0:
        return []
    
    wiki = WikiApi()
    
    info=[]
    for word in keywords:
        results = wiki.find(word)
        others = [x for x in keywords if x!=word]
        
        if search_depth is not None:
            results = results[:search_depth]
        
        for res in results:
            article = wiki.get_article(res)
            summary_words = article.summary.lower().split(' ')
            has_words = any(word in summary_words for word in others)
            
            if has_words:
                info.append(article.heading)
    try:
        info_keyword= gensim.summarization.keywords(' '.join(info),
                                                   words=keyword_summary).split('\n')
    except:
        #print('keyword extraction failed')
        info_keyword =info[:]
    return info_keyword

def main():
    tweets_data = load_json(file_path)

    #Remove URLs from all the tweets in the dataframe
    tweet_text= tweets_data['text'].str.replace(r"http\S+","")

    tweet_text = tweet_text.apply(tokenize_text)
    tweet_text = tweet_text.apply(remove_numbers)
    tweet_text = tweet_text.apply(lemmatize_text)

    k=5
    tweets_lda = LdaModel(text_bagofwords,
                        num_topics = k,
                        id2word = text_dict,
                        random_state =1,
                        passes=10)

    ##Converting from tuuple to dictionary, and remove the weights from each keyword
    tuple_topics = tweets_lda.show_topics()

    topics_dict = {'Topic_' + str(i+1): [token for token, score in tweets_lda.show_topic(i, topn=10)] for i in range(0, tweets_lda.num_topics)}

    for i in topics_dict:
        topic_summary = get_relevant_articles(topics_dict[i])
        print(topic_summary)

main() 
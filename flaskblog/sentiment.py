from datetime import datetime, date, time, timedelta
from collections import Counter
from flaskblog import api
import sys
import tweepy
import numpy as np
import pandas as pd
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


def get_tweets(hashtag):
    all_tweets = []
    for tweet in tweepy.Cursor(api.search, q=hashtag, lang='en', tweet_mode = 'extended').items(100):
        all_tweets.append(tweet.full_text)
    return all_tweets

def tweet_to_data_frame(tweets):
    df = pd.DataFrame(data=[tweet for tweet in tweets], columns=['Tweets'])
    return df

def cleantext(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) #remove mentions
    text = re.sub(r'#', '', text) #remove hashtags
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r"http\S+", "", text)
    text = text.replace('|', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\\', ' ')

    return text

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'

def positivetweets(data):
    positive = data[data.Analysis == 'Positive']
    positive = positive['Tweets']

    return round(positive.shape[0]/data.shape[0]*100, 2)

def negativetweets(data):
    negative = data[data.Analysis == 'Negative']
    negative = negative['Tweets']

    return round(negative.shape[0]/data.shape[0]*100, 2)

def neutraltweets(data):
    neutral = data[data.Analysis == 'Neutral']
    neutral = neutral['Tweets']

    return round(neutral.shape[0]/data.shape[0]*100, 2)

def wordcloud(data):
    allWords = ' '.join([twts for twts in data['Tweets']])
    stopwords = STOPWORDS
    stopwords.add('amp')
    stopwords.add('I')
    stopwords.add('The')
    stopwords.add('us')
    stopwords.add('re')
    stopwords.add('able')
    stopwords.add('give')
    stopwords.add('able')
    stopwords.add('give')
    wordCloud = WordCloud(stopwords=stopwords, width = 800, height = 500, random_state = 21, max_font_size = 100).generate(allWords)

    plt.imshow(wordCloud, interpolation = "bilinear")
    plt.axis("off")
    plt.show()
    
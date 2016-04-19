import csv
import sys
import tweepy
import nltk
from nltk.stem import *
from nltk.corpus import sentiwordnet as swn

CONSUMER_KEY = "oDphrYhTXiYU4WDZim9p9lUYE"
CONSUMER_SECRET = "2n9QGqiMZ2BVAImsQSwv2Aeng93aXc5EUPhr55QyfrqpXrwe0D"
ACCESS_TOKEN = "2267861995-MghGrmkwkeAiDnNi6BNbpQO5gJeQOqpfVkuME6j"
ACCESS_TOKEN_SECRET = "Q6h8qlIK7B1PWT7nEx3nxsrHAVISAwkgz1ttxmLtodGxo"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
time = ["" for x in range(110)] 
screen_names = ["" for x in range(110)]
tweets = ["" for x in range(110)]
retweets = [-1 for x in range(110)]
num_followers = [-1 for x in range(110)]
sentiment = [-1 for x in range(110)]
count = 0

with open('blm.csv', encoding='ascii', errors = "ignore") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        screen_names[count] = row['Screen Name'].replace("@","")
        time[count] = row['Time']
        tweets[count] = (row['Tweet'])
        retweets[count] = row['RT']
        count = count + 1

# get sentiment score of tweets
for x in range(0, len(tweets)):
	tokens = nltk.word_tokenize(tweets[x])
	tagged = nltk.pos_tag(tokens)	# tag tokens for part of speech
	pscore = 0
	nscore = 0

	for i in range(0,len(tagged)):
	    if 'NN' in tagged[i][1] and len(list(swn.senti_synsets(tagged[i][0],'n'))) > 0:
	        pscore+=(list(swn.senti_synsets(tagged[i][0],'n'))[0]).pos_score()
	        nscore+=(list(swn.senti_synsets(tagged[i][0],'n'))[0]).neg_score()
	    elif 'VB' in tagged[i][1] and len(list(swn.senti_synsets(tagged[i][0],'v'))) > 0:
	        pscore+=(list(swn.senti_synsets(tagged[i][0],'v'))[0]).pos_score()
	        nscore+=(list(swn.senti_synsets(tagged[i][0],'v'))[0]).neg_score()
	    elif 'JJ' in tagged[i][1] and len(list(swn.senti_synsets(tagged[i][0],'a'))) > 0:
	        pscore+=(list(swn.senti_synsets(tagged[i][0],'a'))[0]).pos_score()
	        nscore+=(list(swn.senti_synsets(tagged[i][0],'a'))[0]).neg_score()
	    elif 'RB' in tagged[i][1] and len(list(swn.senti_synsets(tagged[i][0],'r'))) > 0:
	        pscore+=(list(swn.senti_synsets(tagged[i][0],'r'))[0]).pos_score()
	        nscore+=(list(swn.senti_synsets(tagged[i][0],'r'))[0]).neg_score()
		
	sentiment[x] = (pscore - nscore)

print(sentiment)
import csv
import sys
import tweepy
import nltk
from nltk.stem import *
from nltk.corpus import sentiwordnet as swn

CONSUMER_KEY = "ECgRrXkQt551Y75hWaEAhuLVB"
CONSUMER_SECRET = "cHbSmCHPJNdpWNlDHUEsQ5vVGKWqaURiSHyKgCsyEf74G7F7c2"
ACCESS_TOKEN = "393600504-kNU18ts1ml7eOpXczWjqfTH2UGM0LqMyRRvkiryu"
ACCESS_TOKEN_SECRET = "HZAQU8fpXc7WKqypHc3agDLjAoboO89jqioTznVpNSbRl"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#with open('testdata.csv', "r", encoding='utf-8') as csvfile:
    #spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    #row_count = sum(1 for row in spamreader)
    #for i in range(10):
        #print(', '.join(spamreader.__next__()).encode('utf-8'))
    #for row in spamreader:
    #    print(', '.join(row).encode('utf-8'))
    
time = ["" for x in range(110)] 
screen_names = ["" for x in range(110)]
tweets = ["" for x in range(110)]
retweets = [-1 for x in range(110)]
num_followers = [-1 for x in range(110)]
sentiment = [-1 for x in range(110)]
count = 0

with open('testdata.csv', encoding='utf-8', 'ignore') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        screen_names[count] = row['Screen Name'].replace("@","")
        time[count] = row['Time']
        tweets[count] = row['Tweet']
        retweets[count] = row['RT']
        count = count + 1

index = 1
user_num = 0
num_foll = 0

<<<<<<< HEAD
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

    #gets number of followers of each user who tweeted with the same hashtag within the time frame after original user's tweet and end of the dataset
    followers = tweepy.Cursor(api.followers, screen_name=screen_names[x]).items()
    while screen_names[index] != screen_names[x] and index != 110:
        if screen_names[index] in followers:
            num_foll = num_foll+1
        index = index + 1
    num_followers[x] = num_foll
    user_num = user_num + 1
    index = user_num + 1
    num_foll = 0

print(sentiment)
print (num_followers)



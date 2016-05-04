import csv
import sys
import tweepy
import nltk
import sys
from array import *
from nltk.stem import *
from nltk.corpus import sentiwordnet as swn

CONSUMER_KEY = "ECgRrXkQt551Y75hWaEAhuLVB"
CONSUMER_SECRET = "cHbSmCHPJNdpWNlDHUEsQ5vVGKWqaURiSHyKgCsyEf74G7F7c2"
ACCESS_TOKEN = "393600504-kNU18ts1ml7eOpXczWjqfTH2UGM0LqMyRRvkiryu"
ACCESS_TOKEN_SECRET = "HZAQU8fpXc7WKqypHc3agDLjAoboO89jqioTznVpNSbRl"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

time = ["" for x in range(100)] 
screen_names = ["" for x in range(int(sys.argv[2]))]
tweets = ["" for x in range(100)]
retweets = [-1 for x in range(100)]
original_followers = [-1 for x in range(100)]
num_followers = [-1 for x in range(100)]
sentiment = [-1 for x in range(100)]
ids = [-1 for x in range(int(sys.argv[2]))]
map_followers = {}
map_followers_rt = {}
count = 0

# read data from csv into arrays
with open(sys.argv[1], encoding='ascii', errors = "ignore") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if count < len(tweets):
            screen_names[count] = row['Screen Name'].replace("@","")
            time[count] = row['Time']
            tweets[count] = row['Tweet']
            retweets[count] = row['RT']
            original_followers[count] = row['Followers']
            count = count + 1
        else:
            screen_names[count] = row['Screen Name'].replace("@","")
            count = count + 1

# traverse through list of tweets to obtain tweet sentiment and 
for x in range(0, len(tweets)):
    # get sentiment score of tweets
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
        elif 'RB' in tagged[i][1] and len(list(swn.senti_synsets(tagged[i][0],'r'))) > 0:
            pscore+=(list(swn.senti_synsets(tagged[i][0],'r'))[0]).pos_score()
            nscore+=(list(swn.senti_synsets(tagged[i][0],'r'))[0]).neg_score()
        elif 'JJ' in tagged[i][1] and len(list(swn.senti_synsets(tagged[i][0],'a'))) > 0:
            pscore+=(list(swn.senti_synsets(tagged[i][0],'a'))[0]).pos_score()
            nscore+=(list(swn.senti_synsets(tagged[i][0],'a'))[0]).neg_score()
    sentiment[x] = (pscore - nscore)

# get associated user id from screen name for all tweets
for x in range(0, len(ids)):
    try:
        temp = api.get_user(screen_name = screen_names[x])
    except tweepy.error.TweepError:
        pass
    ids[x] = temp.id   

# get list of follower ids
for x in range(0, len(tweets)): 
    temp_ids = []
    if (screen_names[x] not in map_followers.keys()):
        try:
            for page in tweepy.Cursor(api.followers_ids, screen_name = screen_names[x]).pages():
                temp_ids.extend(page)
        except tweepy.error.TweepError:
            pass
    map_followers[screen_names[x]] = temp_ids

index = 0
num_foll = 0

# cross reference followers with num people who tweeted with the same hashtag
for x in range(0, len(tweets)):
    temp = [-1 for x in range(600)]
    
    followers = map_followers[screen_names[x]]
    for id in ids:
        if id in followers:
            num_foll = num_foll + 1
            temp[index] = id
            index = index + 1
    num_followers[x] = num_foll
    num_foll = 0
    map_followers_rt[screen_names[x]] = list(set(temp))
    index = 0

# write to csv file
with open('makeamericagreat_final.csv', 'w', newline = '') as csvfile:
    for x in range(0, len(tweets)):
        writer = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        writer.writerow([screen_names[x], retweets[x] ,time[x], sentiment[x], original_followers[x], num_followers[x], ids[x], map_followers_rt[screen_names[x]]])
    for y in range(100, len(ids)):
        writer = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        writer.writerow(['', '','', '','', '', ids[y]]) 


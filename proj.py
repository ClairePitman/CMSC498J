import csv
import sys
import tweepy

CONSUMER_KEY = "oDphrYhTXiYU4WDZim9p9lUYE"
CONSUMER_SECRET = "2n9QGqiMZ2BVAImsQSwv2Aeng93aXc5EUPhr55QyfrqpXrwe0D"
ACCESS_TOKEN = "2267861995-MghGrmkwkeAiDnNi6BNbpQO5gJeQOqpfVkuME6j"
ACCESS_TOKEN_SECRET = "Q6h8qlIK7B1PWT7nEx3nxsrHAVISAwkgz1ttxmLtodGxo"

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
count = 0

with open('testdata.csv', encoding='utf-8') as csvfile:
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


#for user in screen_names:
followers = tweepy.Cursor(api.followers, screen_name=screen_names[user_num]).items()
while screen_names[index] != screen_names[0] and index != 110:
    if screen_names[index] in followers:
        num_foll = num_foll+1
print(num_foll)
index = index + 1
num_followers[user_num] = num_foll
user_num = user_num + 1
index = user_num + 1
num_foll = 0
    
    
#print(num_foll)
#for user in tweepy.Cursor(api.followers, screen_name=screen_names[0]).items():
#    print(user.screen_name)

#print(screen_names)
#print(tweets[0])
#print(time[0])
#print(retweets[0])

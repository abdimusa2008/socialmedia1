import time
import tweepy

from credentials import*



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

api = tweepy.API(auth)

ids = []
for page in tweepy.Cursor(api.followers_ids, screen_name="xalka_somaliya").pages():
    
    ids.extend(page)
    time.sleep(60)

print (len(ids))
# This file contains all the utility methods

#!/bin/user/python

#import required libraries
import signal
import sys
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# File path where fetched data will be stored
FILEPATH="../data/twitter_data.txt"

# Secret File Path
SECRETFILEPATH="../secret/auth.txt"

# Fetch the access token and consumer key from secret folder
def fetch_secret():

    f = open(SECRETFILEPATH, 'r')
    authdict = {}

    for data in f.readlines():
        list = data.split("=")
        authdict[list[0]] = list[1].strip()

    access_token        = authdict['access_token']
    access_token_secret = authdict['access_token_secret']
    consumer_key        = authdict['consumer_key']
    consumer_secret     = authdict['consumer_secret']

	# Attempt Authentication 
#	try:
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return auth
#	except:
	#	print("Error: Authentication Failed")
	#	return -1

# Number of tweets captured
def GetNumOfTweets():
    f = open(FILEPATH, "r")
    count = 0
    for i in f.readlines():
        count = count + 1

    print(str(count)+" Tweets fetched !")
    f.close()

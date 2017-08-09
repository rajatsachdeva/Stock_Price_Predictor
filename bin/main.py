#!/bin/user/python

'''
	Stock Price Prediction
'''
import signal
import sys
import time
import fetch_csv as fc
from tweet_analyser import TwitterClient

# Signal Handler
def exit_gracefully(signum, frame):
	# restore the original signal handler as otherwise evil things will happen
	# in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
	signal.signal(signal.SIGINT, original_sigint)
	try:
		if input("\nReally quit? (y/n)> ").lower().startswith('y'):
			print("Shutting down...")
			sys.exit(1)
			
	except KeyboardInterrupt:
		print("Ok ok, quitting")
		sys.exit(1)

# restore the exit gracefully handler here    
signal.signal(signal.SIGINT, exit_gracefully)

# Main Function
def main():
	
	# store the original SIGINT handler
	original_sigint = signal.getsignal(signal.SIGINT)

	print("Starting Stock Price Prediction Program...\n")
	# Go in Event Loop
	while input("Enter (y/n)> ").lower().startswith('y'):

		# Take input query from user 
		stock = input("\nEnter Stock Symbol (Like GOOG, AAPL etc.): ")

		# Fetch stock csv from google finance
		fc.fetch_stock_csv(stock)

		# creating object of TwitterClient Class
		api = TwitterClient()

		# calling function to get tweets
		tweets = api.get_tweets(query = stock, count = 2000)

		# picking positive tweets from tweets
		ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

		# picking negative tweets from tweets
		ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

		print("\nPostive Tweets: {}".format(len(ptweets)))
		print("\nNegative Tweets: {}".format(len(ntweets)))

	print("Exiting from program...")
if __name__ == '__main__': 
	main()

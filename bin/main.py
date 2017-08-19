#!/Users/rohanrajat/anaconda/bin/python

'''
	Stock Price Prediction
'''
import signal
import sys
import time
import fetch_csv as fc
import utils as ut
from tweet_analyser import TwitterClient
import logging
import log_init

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
	log_init.initialize_logger('../log', False)

	print("Starting Stock Price Prediction Program...\n")
	# Go in Event Loop
	while input("Enter (y/n)> ").lower().startswith('y'):

		# Take input query from user 
		stock 	= input("\nEnter Stock Symbol (Like GOOG, AAPL etc.): ")
		days 	= int(input("\nEnter number of days for which data is to fetched: "))

		result, conn_error, ptweets, ntweets, predicted_price_rbf, predicted_price_keras = ut.stock_price_predictor(stock, days)

		if conn_error & (not result):
			print("Connection Error: Please check you Internet Connection")
		elif result & (not conn_error):
			print("\n**** RESULT *****\n")
			print("Postive Tweets: {}".format(len(ptweets)))
			print("Negative Tweets: {}".format(len(ntweets)))
			
			print("\n ** Prediction **\n")
			print("Current price: {}".format(ut.get_recent_price(stock)))
			print("RBF: {}".format(predicted_price_rbf))
			print("KERAS: {}".format(predicted_price_keras))
		else:
			print("\n Please validate the stock symbol/days input")

	# End of while Loop		
	
	print("Exiting from program...")
if __name__ == '__main__': 
	main()

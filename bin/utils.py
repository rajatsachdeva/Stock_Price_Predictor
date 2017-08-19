# This file contains all the utility methods

#!/Users/rohanrajat/anaconda/bin/python

#import required libraries
import csv, os, signal, sys, time, logging
# fetch csv related imports
import fetch_csv as fc
import fetch_yahoo_csv as fcy
# os functions related
from os import listdir
from os.path import join
# Pillow package imports
from PIL import Image, ImageTk
# tweet related imports
from tweet_analyser import TwitterClient
from tweepy import OAuthHandler
from tweepy import Stream
# matplotlib imports
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
# sklearn imports
from sklearn.svm import SVR
# keras imports
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import CSVLogger

# Secret File Path
SECRET_FILE_PATH 	= "../secret/auth.txt"

# csv Path file
CSV_FILE_PATH 		= "../csv_data/{}.csv"
CSV_LOG_FILE_PATH	= "../log/log.csv"

# Output Graph Path
OUTPUT_GRAPH_PATH 	= "../output_graphs/"

# RBF/KERAS image Name
RBF_FN				= "{}_rbf.png"
KERAS_FN_PNG		= "{}_keras.png"
KERAS_FN_JPG		= "{}_keras.jpg"
TREND_FN			= "{}_trend.png"

# For Suppressing the warnings 
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# Fetch the access token and consumer key from secret folder
def fetch_secret():
	logging.info("Fetching Secret...")
	f = open(SECRET_FILE_PATH, 'r')
	authdict = {}

	for data in f.readlines():
		list = data.split("=")
		authdict[list[0]] = list[1].strip()

	access_token        = authdict['access_token']
	access_token_secret = authdict['access_token_secret']
	consumer_key        = authdict['consumer_key']
	consumer_secret     = authdict['consumer_secret']

	# Construct Authentication key
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	return auth

# Predict using SVM (Support Vector Model) RBF 
def predict_rbf(stock, dates, prices, x):
	dates 	= [ i+1 for i in range(len(prices)) ]
	dates 	= np.reshape(dates,(len(dates), 1)) # converting to matrix of n X 1
	svr_rbf = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1) # defining the support vector regression models
	svr_rbf.fit(dates, prices) # fitting the data points in the models

	plt.scatter(dates, prices, color= 'black', label= 'Data') # plotting the initial datapoints 
	plt.plot(dates, svr_rbf.predict(dates), color= 'red', label= 'RBF model') # plotting the line made by the RBF kernel
	plt.scatter([len(dates) +1 ], svr_rbf.predict(x)[0], color = 'blue', label = 'RBF Prediction')
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title('Support Vector Regression')
	plt.legend()
	plt.savefig(OUTPUT_GRAPH_PATH + RBF_FN.format(stock))
	logging.info("Graph saved as {}_rbf.png in ../output_graphs".format(stock))
	logging.info("RBF: Last price was {} , predicted price is {}".format(prices[len(prices)-1], svr_rbf.predict(x)[0]))
	return svr_rbf.predict(x)[0]

# Prediction using Keras
def predict_keras(stock):

	csv_logger 	= CSVLogger(CSV_LOG_FILE_PATH, append=False, separator=';')

	# Collect data points from csv
	dataset 	= []
	logging.info("Getting dataset from csv file")
	with open(CSV_FILE_PATH.format(stock)) as f:
		for n, line in enumerate(f):
			if n != 0:
				x = line.split(',')[1]
				if x == '-':
					continue
				dataset.append(x)

	dates 	= [ i+1 for i in range(len(dataset)) ]
	prices 	= dataset[::-1]
	dataset = np.array(dataset)

	# Create dataset matrix (X=t and Y=t+1)
	def create_dataset(dataset):
		dataX = [dataset[n+1] for n in range(len(dataset)-2)]
		return np.array(dataX), dataset[2:]
		
	trainX, trainY = create_dataset(dataset)

	# Create and fit Multilinear Perceptron model
	model = Sequential()
	model.add(Dense(8, input_dim=1, activation='relu'))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')

	# verbose = 0 for not displaying epoch loss data on console
	model.fit(trainX, trainY, epochs=200, batch_size=2, verbose=0, callbacks=[csv_logger])
	
	# Our prediction for tomorrow
	prediction = model.predict(np.array([dataset[0]]))
	
	# converting to matrix of n X 1
	dates = np.reshape(dates,(len(dates), 1)) 
	
	# Plot the prediction on graph
	plt.plot(dates, prices, color='green', label='Price Trend')
	plt.scatter([len(dates) + 1], prediction, color= 'red', label= 'Keras Prediction') # plotting the line made by the RBF kernel
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title('Price Prediction for {}'.format(stock))
	plt.legend()
	plt.savefig(OUTPUT_GRAPH_PATH + KERAS_FN_PNG.format(stock))

	# convert the saved figure format from .png to .jpg
	im 		= Image.open(OUTPUT_GRAPH_PATH + KERAS_FN_PNG.format(stock))
	rgb_im 	= im.convert('RGB')
	rgb_im.save(OUTPUT_GRAPH_PATH + KERAS_FN_JPG.format(stock),'JPEG')
	plt.clf()
	logging.info('The price will move from %s to %s' % (dataset[0], prediction[0][0]))
	result 	= prediction[0][0]
	return result

# get data from the csv file and store in the price/dates list
def get_data(filename, dates, prices):
	with open(filename, 'r') as csvfile:
		csvFileReader = csv.reader(csvfile)
		# Skip first row , that contains the columns names
		next(csvFileReader)
		for row in csvFileReader:
			# Get only the Date from the date and append in date list
			if (row[1] == '-'):
				continue
			prices.append(float(row[1]))
			dates.append(int(row[0].split('-')[0]))
	return

# Function to clean/Delete particular type of files in a directory
def cleanup(directory, extension):
	logging.info("Cleanup: Deleting all files in {} with extension {}".format(directory, extension))
	contents = os.listdir(directory)
	logging.info("Number of items in {}: {}".format(directory, len(contents)))
	for item in contents:
		if item.endswith(extension):
			os.remove(join(directory, item))

# predict_price
# IN
#	- stock 	: stock symnol like GOOG, AAPL etc.
#	- dates 	: dates list
# 	- price_list: list of prices for the stock
# 	- x			: Date for which the price is to be predicted
def predict_price(stock, dates, price_list, x, mode='both'):
	logging.info("Length of price list is {}".format(len(price_list)))
	# Plot Trend for stock 
	plt.plot(price_list)
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title('{} Price Trend'.format(stock))
	plt.savefig(OUTPUT_GRAPH_PATH + TREND_FN.format(stock))
	plt.clf()
	logging.info(TREND_FN.format(stock) + " image saved in " + OUTPUT_GRAPH_PATH)
	
	if mode == 'both':
		logging.info('Getting prediction from both models')

		logging.info ('*******  RBF ********')
		predicted_price_rbf = predict_rbf(stock, dates, price_list, x)

		logging.info ('******* TENSORFLOW ********')
		predicted_price_keras = predict_keras(stock)

		# return predictions
		return predicted_price_rbf, predicted_price_keras

def stock_price_predictor(stock, no_of_days=30, mode='both'):
	# Positive/Negative Tweets list
	ptweets 				= []
	ntweets 				= []
	# Prediction variables
	predicted_price_rbf 	= 0.0
	predicted_price_keras	= 0.0

	# connection error
	conn_error				= False

	# Fetch stock csv from google finance if not present there, then from yahoo finance
	result , conn_error = fc.fetch_stock_csv(stock, no_of_days)

	# Check if there is connection error 
	if conn_error:
		logging.warning("Error while fetching data: No Internet Connection")
		return False, conn_error, ptweets, ntweets, predicted_price_rbf, predicted_price_keras

	if not result:
		logging.warning("Error while fetching stock ({}) data from google.Trying from yahoo".format(stock))
		if not fcy.get_stock_yahoo(stock, no_of_days):
			logging.warning("Error while fetching stock from yahoo")
			return False, conn_error, ptweets, ntweets, predicted_price_rbf, predicted_price_keras

	logging.info("*** Tweets fetching ***")
	# creating object of TwitterClient Class
	api 	= TwitterClient()

	# calling function to get tweets
	tweets 	= api.get_tweets(query = stock.split('.')[0], count = 200 * no_of_days)

	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

	# picking negative tweets from tweets
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

	logging.info("\nPostive Tweets: {}".format(len(ptweets)))
	logging.info("\nNegative Tweets: {}".format(len(ntweets)))

	dates 	= []
	prices 	= []
	get_data(CSV_FILE_PATH.format(stock), dates, prices)

	# Reverse the list entries to represent from start to today
	prices 	= prices[::-1]

	# get the predicted prices from rbf, Keras
	predicted_price_rbf ,predicted_price_keras = predict_price(stock, dates, prices, len(prices), mode)
	logging.info("\n*** RESULT ***\nPrediction from RBF : {}".format(predicted_price_rbf))
	logging.info("Prediction from keras: {}".format(predicted_price_keras))
	# return result
	return True, conn_error, ptweets, ntweets, predicted_price_rbf, predicted_price_keras 

def get_recent_price(stock):
	logging.info("fetching the last open price for {}".format(stock))
	with open(CSV_FILE_PATH.format(stock)) as f:
		for n, line in enumerate(f):
			if n != 0:
				return float(line.split(',')[1])



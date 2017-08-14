# This file contains all the utility methods

#!/bin/user/python

#import required libraries
import csv
import os
import signal
import sys
import time
from os import listdir
from os.path import join
from PIL import Image, ImageTk
from tweepy import OAuthHandler
from tweepy import Stream
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVR
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import CSVLogger
import logging
logger = logging.getLogger(__name__)

# Secret File Path
SECRETFILEPATH="../secret/auth.txt"

# For Suppressing the warnings 
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# Fetch the access token and consumer key from secret folder
def fetch_secret():
	print("Fetching Secret...")
	f = open(SECRETFILEPATH, 'r')
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

# Function to plot the price trend for given stock 
# and save in ../output_graphs/stock.jpg
def plot_price_trend(stock, prices):
	pass

# Predict using SVM (Support Vector Model) RBF 
def predict_rbf(stock, dates, prices, x):
	dates = [ i+1 for i in range(len(prices)) ]
	#print("RBF: dates: ", dates)
	dates = np.reshape(dates,(len(dates), 1)) # converting to matrix of n X 1
	svr_rbf = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1) # defining the support vector regression models
	svr_rbf.fit(dates, prices) # fitting the data points in the models

	plt.scatter(dates, prices, color= 'black', label= 'Data') # plotting the initial datapoints 
	plt.plot(dates, svr_rbf.predict(dates), color= 'red', label= 'RBF model') # plotting the line made by the RBF kernel
	plt.scatter([len(dates) +1 ], svr_rbf.predict(x)[0], color = 'blue', label = 'RBF Prediction')
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title('Support Vector Regression')
	plt.legend()
	plt.savefig("../output_graphs/{}_rbf.png".format(stock))
	#plt.clf()
	print("Graph saved as {}_rbf.jpg in ../output_graphs".format(stock))
	print("RBF: Last price was {} , predicted price is {}".format(prices[len(prices)-1], svr_rbf.predict(x)[0]))
	return svr_rbf.predict(x)[0]

# Prediction using Keras
def predict_keras(stock):

	csv_logger = CSVLogger('../log/log.csv', append=False, separator=';')

	# Collect data points from csv
	dataset = []

	print("Getting dataset from csv file")
	with open("../csv_data/{}.csv".format(stock)) as f:
		for n, line in enumerate(f):
			if n != 0:
				x = line.split(',')[1]
				if x == '-':
					continue
				dataset.append(x)

	dates = [ i+1 for i in range(len(dataset)) ]
	prices = dataset[::-1]
	dataset = np.array(dataset)
	#print("dataset = ",dataset)

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
	
	dates = np.reshape(dates,(len(dates), 1)) # converting to matrix of n X 1
	
	plt.plot(dates, prices, color='green', label='Price Trend')
	plt.scatter([len(dates) + 1], prediction, color= 'red', label= 'Keras Prediction') # plotting the line made by the RBF kernel
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title('Tensor Flow Method')
	plt.legend()
	plt.savefig("../output_graphs/{}_keras.png".format(stock))
	# convert the saved figure format from .png to .jpg
	im = Image.open("../output_graphs/{}_keras.png".format(stock))
	rgb_im = im.convert('RGB')
	rgb_im.save("../output_graphs/{}_keras.jpg".format(stock),'JPEG')
	plt.clf()
	print('The price will move from %s to %s' % (dataset[0], prediction[0][0]))

	result = prediction[0][0]
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
	print("Cleanup: Deleting all files in {} with extension {}".format(directory, extension))
	logging.debug("Cleanup: Deleting all files in {} with extension {}".format(directory, extension))
	contents = os.listdir(directory)
	logging.info("Number of items in {}: {}".format(directory, len(contents)))
	for item in contents:
		if item.endswith(extension):
			os.remove(join(directory, item))

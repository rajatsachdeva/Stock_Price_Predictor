'''
 This API Fetches Historical Prices for a given Stock
 from Google finance either from 
 	NASDAQ, 
 	NYSE, 
 	S&P, 
 	DOWJONES,
 	BSE,
 	NSE
 	etc
 As .csv file and saves it in ../csv_data directory
 as STOCK.csv
'''

#!/bin/user/python

# Required imports
import os
import csv
import requests
from requests.exceptions import ConnectionError
from datetime import datetime
from datetime import timedelta
import logging


# List Stock Exchanges
# Reference: https://en.wikipedia.org/wiki/List_of_stock_exchanges
# You can add in the following list required stock exchanges
stock_exchange 		= [ "NASDAQ", "NYSE", "CAC"]

# base url for creating the google finance link
base_url       		= "http://www.google.com/finance/historical"

# CSV file save location
csv_file_location 	= "../csv_data/"

# Function to create the url for fetching the csv file from google finance
# IN
# 	- _stock: 			Stock symbol
#	- _stock_exchange:  Stock exchange symbol
# 	- startdate:		Start date from which data is to be fetched 
# 	- enddate:			End date to which data is to be fetched
#
def make_url(_stock, _stock_exchange = "NASDAQ", no_of_days=30):
	global base_url

	logging.info("Construct url")
	# Get the current date in format Mon+day+year
	enddate = datetime.now().strftime('%b+%-d+%Y')
	logging.info("enddate = {}".format(enddate))

	# Get 30 days before date from today in format Mon+day+year
	startdate = datetime.now() - timedelta(days = no_of_days)
	startdate = startdate.strftime('%b+%-d+%Y')
	logging.info("startdate = {}".format(startdate))

	full_url = base_url + "?q=" + _stock_exchange + "%3A" + _stock
	full_url = full_url + "&startdate={}&enddate={}".format(startdate, enddate) + "&output=csv"
	return full_url

# Function to fetch the csv file from google finance and save in 
def fetch_csv(stock, url):
	conn_error = False
	try:
		response = requests.get(url)
		with open(os.path.join("../csv_data", "{}.csv".format(stock)), 'wb') as f:
			f.write(response.content)
		f.close()
		return conn_error

	except ConnectionError: 
		logging.warning("Seems to a Connection Error")
		conn_error = True
		return conn_error

# Function to check if stock data was fetched correctly
def check_if_fetched_stock_data(csvfilename):
	error_string = "The requested URL was not found on this server"
	f = open(csvfilename, "rb")
	for data in f:
		# Check if error is present
		if error_string in str(data):
			f.close()
			return False
		else:
			f.close()
			return True

def fetch_stock_csv(stock, no_of_days=30):
	for se in stock_exchange:

		conn_error = False

		# construct url
		logging.info("Constructing url for stock: {} with stock exchange as {}".format(stock, se))
		url = make_url(_stock = stock, _stock_exchange = str(se), no_of_days = no_of_days)
		logging.info("Fetching information for {} from \nurl: {}".format(stock, url))

		# Fetch data from constructed url
		conn_error = fetch_csv(stock, url)
		if conn_error:
			return False, conn_error

		Found = 0

		# Check if fetched data is valid
		csvfilename = csv_file_location + "{}.csv".format(stock)
		if check_if_fetched_stock_data(csvfilename):
			Found = 1
			break
		else:
			logging.warning("Error while fetching, checking from next stock exchange")

	if Found:
		logging.info("csv file is saved at location " + csvfilename)
		return True, conn_error
	else:
		logging.warning("ERROR: Please validate the stock symbol/Update the Stock Exchange list...")
		return False, conn_error
			
if __name__ == "__main__":
	stock = input("Enter Stock Symbol (Like: GOOG, AAPL, etc): ").upper()
	print (fetch_stock_csv(stock))
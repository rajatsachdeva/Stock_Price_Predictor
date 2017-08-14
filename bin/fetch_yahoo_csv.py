# Program to fetch the data from yahoo finance and store the csv file

import pandas_datareader as web
from pandas_datareader._utils import RemoteDataError
from datetime import datetime
from datetime import timedelta
import logging

def get_stock_yahoo(stock, no_of_days=30):

	startdate = datetime.now() - timedelta(days = no_of_days)
	enddate = datetime.now()
	print("enddate = {}".format(enddate))
	logging.debug("enddate = {}".format(enddate))
	print("startdate = {}".format(startdate))
	logging.debug("startdate = {}".format(startdate))

	try:
		web.DataReader(stock, 'yahoo', startdate, enddate).to_csv('../csv_data/{}.csv'.format(stock))
		logging.debug("Got the data")
		return True
	except RemoteDataError as e:
		logging.warning("Didn't get the data, ", e)
		print(e)
		return False

def main():
	while input("Enter (y/n)> ").lower().startswith('y'):
		stock = input("Enter Stock: ")
		print (get_stock_yahoo(stock))

if __name__ == "__main__":
	main()
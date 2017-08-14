#!/Users/rohanrajat/anaconda/bin/python

import os
import tkinter as tk
import fetch_csv as fc
import fetch_yahoo_csv as fcy
import utils as ut 
from tweet_analyser import TwitterClient
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PIL import Image, ImageTk
import logging
logger = logging.getLogger(__name__)

ptweets = []
ntweets = []

# Prediction prices
predicted_price_rbf 	= 0.0
predicted_price_keras 	= 0.0

def predict_price(stock, dates, price_list, x, mode='both'):
	global predicted_price_rbf
	global predicted_price_keras

	y = price_list
	logging.info("Length of price list is {}".format(len(price_list)))
	
	plt.plot(y)
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.title('{} Price Trend'.format(stock))
	plt.savefig("../output_graphs/{}_trend.png".format(stock))
	plt.clf()
	
	if mode == 'both':
		print ('Getting prediction from both models')

		print ('\t\t*******\t\t  RBF \t\t********')
		predicted_price_rbf = ut.predict_rbf(stock, dates, price_list, x)

		print ('\n\n\t\t*******\t\t  TENSORFLOW \t\t********')
		predicted_price_keras = ut.predict_keras(stock)

def stock_price_predictor(stock, no_of_days=30, mode='both'):
	global ptweets
	global ntweets
	global predicted_prices

	# Fetch stock csv from google finance if not present there, then from yahoo finance
	if not fc.fetch_stock_csv(stock, no_of_days):
		print("Error while fetching stock ({}) data from web.Please check Stock Symbol".format(stock))
		if not fcy.get_stock_yahoo(stock, no_of_days):
			return False

	# creating object of TwitterClient Class
	api = TwitterClient()

	# calling function to get tweets
	tweets = api.get_tweets(query = stock.split('.')[0], count = 50000)

	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

	# picking negative tweets from tweets
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

	print("\nPostive Tweets: {}".format(len(ptweets)))
	print("\nNegative Tweets: {}".format(len(ntweets)))

	dates = []
	prices = []
	ut.get_data("../csv_data/{}.csv".format(stock), dates, prices)

	# Reverse the list entries to represent from start to today
	prices = prices[::-1]

	# print the predicted prices from rbf, Keras
	predict_price(stock, dates, prices, len(prices) + 1, mode)

	print("\nPrediction from RBF : {}".format(predicted_price_rbf))

	return True

# Create a Class for GUI
class simpleapp_tk():
	global ptweets
	global ntweets
	global predicted_price_rbf
	global predicted_price_keras

	def __init__(self, master):
		self.master = master
		master.title("Stock Price Predictor")
		self.initialize()

	# Initialize Function will have 
	# Buttons, widgets etc.
	def initialize(self):
		print("Initializing...")

		# Create label for Text box
		self.label1 = tk.Label(master=self.master, text='Stock Symbol ').grid(row=0, sticky='W')
		self.label2 = tk.Label(master=self.master, text='Number of Days ').grid(row=1, sticky='W')

		# Create variable to take input from text box of string type
		self.entry_stock_name = tk.StringVar()
		self.no_of_days = tk.StringVar()

		# Link variable name with textbox entry
		self.entry_sn = tk.Entry(master=self.master, textvariable=self.entry_stock_name)
		self.entry_days = tk.Entry(master=self.master, textvariable=self.no_of_days)

		# Place text box
		self.entry_sn.grid(row=0, column=1, sticky='WE')
		self.entry_days.grid(row=1, column=1, sticky='WE')

		# Bind with Enter press event
		self.entry_sn.bind("<Return>", self.OnPressEnter)
		self.entry_days.bind("<Return>", self.OnPressEnter)

		# Create Buttons
		b_predict = tk.Button(self.master, text=u"Predict !", 
							command=self.OnButtonClick)
		b_quit = tk.Button(self.master, text=u"Quit", 
							command=self.master.quit)

		# Place the buttons
		b_predict.grid(column=0,row=3)
		b_quit.grid(column=1,row=3)

		self.labelVariable = tk.StringVar()
		
		label = tk.Label(self.master,textvariable=self.labelVariable, anchor="w",fg="white",bg="blue")
		label.grid(column=0,row=4,columnspan=2, sticky='EW')

		self.labelVariable.set(u"Report will be generated here :)")

		self.master.grid_columnconfigure(0,weight=2)

		self.master.resizable(True,False)

	def OnButtonClick(self):
		stock = self.entry_stock_name.get().upper()
		days = self.entry_days.get()

		# Validate input variable 
		result, output, days = self.validate_text_entry(stock, days)

		if result:
			print("stock name is {}".format(stock))
			print("Number of days :{}".format(days))

			self.generate_output(stock, days)

			print ("You clicked the button !")

		else: 
			self.labelVariable.set(output)
	
	def OnPressEnter(self,event):

		stock = self.entry_stock_name.get().upper()
		days  = self.entry_days.get()

		# Validate input variable 
		result, output, days = self.validate_text_entry(stock, days)

		if result:
			print("stock name is {}".format(stock))
			print("Number of days :{}".format(days))
			
			self.generate_output(stock, days)
			print ("You pressed enter !")

		else:
			self.labelVariable.set(output)

	# validate text input from user 
	def validate_text_entry(self, stock, days):
		out = ''
		result = True

		# validate days type
		if days == '':
			days = 30
		else:
			days = int(days)

		if stock == '':
			print("ERROR: User entered empty Stock Symbol")
			out = out + "Error: Please Enter a valid Stock Symbol"
			return False, out, days

		if days == 30:
			out = "INFO: Program will continue to compute data for past 30 days as default"
			print(out)
			return True, out, days
			
		return result, out, days

	# Function to generate output
	def generate_output(self, stock , days):
		print("Generating output for Stock: {} with {} days".format(stock, days))
		logging.info("Generating output for Stock: {} with {} days".format(stock, days))
		self.labelVariable.set("Please wait while we fetch response")

		# call the Stock Predictor
		if not stock_price_predictor(stock, days):
			logging.warning("No data found from google finance")
			# Fetch from yahoo finance now
			logging.warning("No data found from yahoo finance")
			out = "Error while fetching stock ({}) data from web.Please check Stock Symbol".format(stock)
			logging.warning(out)
			self.labelVariable.set(out)
			return 

		self.labelVariable.set("Postive Tweets: {}".format(len(ptweets))
			+ "\nNegative Tweets: {}".format(len(ntweets))
			+"\nPredicted Price from RBF: {}".format(predicted_price_rbf)
			+"\nPredicted Price from KERAS: {}".format(predicted_price_keras))

		result_graph = ImageTk.PhotoImage(file = '../output_graphs/{}_keras.jpg'.format(stock))
		self.label_graph = tk.Label(self.master, image=result_graph)
		self.label_graph.image = result_graph 
		self.label_graph.grid(row = 6, column = 0, columnspan = 10, sticky="NEWS")

# Create Main()
def main():
	FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)s()] - %(message)s'
	logging.basicConfig(filename = "../log/stock_predictor.log", level=logging.DEBUG, format=FORMAT)

	print("Starting Program...")
	logging.debug("Starting Program...")

	root = tk.Tk()

	# Create the Tk app instance
	app = simpleapp_tk(root)

	print("Starting GUI Application")
	logging.debug("Starting GUI Application")
	print("Going in Event Loop")
	logging.debug("Going in Event Loop")

	# Start the main loop
	root.mainloop()

	# Exit from mainloop
	print("Exting from main loop")
	logging.debug("Exting from main loop")

	# Initiate Cleanup for unused files
	print("Cleanup started")
	logging.debug("Cleanup started")
	ut.cleanup("../csv_data", ".csv")
	ut.cleanup("../output_graphs", ".png")

# Call Main
if __name__ == "__main__":
	main()
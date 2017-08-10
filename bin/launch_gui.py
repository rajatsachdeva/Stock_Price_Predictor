#!/Users/rohanrajat/anaconda/bin/python

import os
import tkinter
import fetch_csv as fc
from tweet_analyser import TwitterClient

ptweets = []
ntweets = []

def StockPredictor(stock):
	global ptweets
	global ntweets

	# Take input query from user 
	#stock = input("\nEnter Stock Symbol (Like GOOG, AAPL etc.): ")

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


# Create a Class for GUI
class simpleapp_tk(tkinter.Tk):
	global ptweets
	global ntweets
	def __init__(self, parent):
		tkinter.Tk.__init__(self, parent)
		self.parent = parent
		self.initialize()

	# Initialize Function will have 
	# Buttons, widgets etc.
	def initialize(self):
		self.grid()

		self.entryVariable = tkinter.StringVar()
		self.entry = tkinter.Entry(self, textvariable=self.entryVariable)
		self.entry.grid(column=0,row=0,sticky='EW')

		self.entry.bind("<Return>", self.OnPressEnter)
		self.entryVariable.set(u"Enter Stock Symbol")

		button = tkinter.Button(self,text=u"Predict !", 
							command=self.OnButtonClick)
		button.grid(column=1,row=0)

		self.labelVariable = tkinter.StringVar()
		
		label = tkinter.Label(self,textvariable=self.labelVariable, anchor="w",fg="white",bg="blue")
		label.grid(column=0,row=2,columnspan=2,sticky='EW')

		self.labelVariable.set(u"Report will be generated here :)")

		self.grid_columnconfigure(0,weight=1)

		self.resizable(True,True)

	def OnButtonClick(self):
		#self.labelVariable.set("You clicked the button !")
		#self.labelVariable.set( self.entryVariable.get()+" (You clicked the button)" )
		stock = self.entryVariable.get()
		print("stock name is {}".format(stock))

		# call the Stock Predictor
		StockPredictor(stock)

		#self.labelVariable.set( self.entryVariable.get() )
		self.labelVariable.set("Postive Tweets: {}".format(len(ptweets))
		 		+ "\nNegative Tweets: {}".format(len(ntweets)))
		print ("You clicked the button !")
	
	def OnPressEnter(self,event):
		#self.labelVariable.set("You pressed enter !")
		#self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
		stock = self.entryVariable.get()
		print("stock name is {}".format(stock))

		self.labelVariable.set("Please wait while we fetch response")

		# call the Stock Predictor
		StockPredictor(stock)

		#self.labelVariable.set( self.entryVariable.get() )
		self.labelVariable.set("Postive Tweets: {}".format(len(ptweets))
		 		+ "\nNegative Tweets: {}".format(len(ntweets)))

		print ("You pressed enter !")


# Create Main
if __name__ == "__main__":
	
	# Create the Tk app instance
	app = simpleapp_tk(None)
	
	# Title for the GUI app
	app.title('Stock Price Predictor')

	print("Starting GUI Application")
	print("Going in Event Loop")

	# Start the main loop
	app.mainloop()

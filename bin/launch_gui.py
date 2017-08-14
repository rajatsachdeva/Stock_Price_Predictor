#!/Users/rohanrajat/anaconda/bin/python

import tkinter as tk
import utils as ut 
from PIL import Image, ImageTk
import log_init
import logging

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
		logging.info("Initializing GUI using tkinter")

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

		logging.info("GUI init successful")

	def OnButtonClick(self):
		logging.info("EVENT: Button was clicked")
		stock = self.entry_stock_name.get().upper()
		days = self.entry_days.get()

		# Validate input variable 
		result, output, days = self.validate_text_entry(stock, days)

		if result:
			logging.info("stock name is {}".format(stock))
			logging.info("Number of days :{}".format(days))
			logging.debug("send parameters for computation")
			self.generate_output(stock, days)

		else: 
			self.labelVariable.set(output)
	
	def OnPressEnter(self,event):
		logging.info("EVENT: Enter was pressed")
		stock = self.entry_stock_name.get().upper()
		days  = self.entry_days.get()

		# Validate input variable 
		result, output, days = self.validate_text_entry(stock, days)

		if result:
			logging.info("stock name is {}".format(stock))
			logging.info("Number of days :{}".format(days))
			logging.debug("send parameters for computation")
			self.generate_output(stock, days)
			
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
			logging.warning("ERROR: User entered empty Stock Symbol")
			out = out + "Error: Please Enter a valid Stock Symbol"
			return False, out, days

		if days == 30:
			out = "INFO: Program will continue to compute data for past 30 days as default"
			logging.warning(out)
			return True, out, days
			
		return result, out, days

	# Function to generate output
	def generate_output(self, stock , days):
		# Positive/Negative Tweets list
		ptweets 				= []
		ntweets 				= []
		# Prediction variables
		predicted_price_rbf 	= 0.0
		predicted_price_keras	= 0.0
		# resultant variable
		result 					= False

		logging.info("Generating output for Stock: {} with {} days".format(stock, days))
		self.labelVariable.set("Please wait while we fetch response")

		# get the result from stock price pridector
		result, ptweets, ntweets, predicted_price_rbf, predicted_price_keras = ut.stock_price_predictor(stock, days)

		# call the Stock Predictor
		if not result:
			logging.warning("No data found from google finance")
			# Fetch from yahoo finance now
			logging.warning("No data found from yahoo finance")
			out = "Error while fetching stock ({}) data from web.Please check Stock Symbol".format(stock)
			logging.warning(out)
			self.labelVariable.set(out)
			return 

		self.labelVariable.set("Postive Tweets: {}".format(len(ptweets))
			+ "\t\tNegative Tweets: {}".format(len(ntweets))
			+ "\nOpening Price for {}: {}".format(stock, ut.get_recent_price(stock))
			+"\nPredicted Price from RBF: {}".format(predicted_price_rbf)
			+"\nPredicted Price from KERAS: {}".format(predicted_price_keras))

		result_graph = ImageTk.PhotoImage(file = ut.OUTPUT_GRAPH_PATH + ut.KERAS_FN_JPG.format(stock))
		self.label_graph = tk.Label(self.master, image=result_graph)
		self.label_graph.image = result_graph 
		self.label_graph.grid(row = 6, column = 0, columnspan = 10, sticky="NEWS")

# Create Main()
def main():
	# initialize logger
	log_init.initialize_logger('../log')

	logging.info("Starting Program...")

	root = tk.Tk()

	# Create the Tk app instance
	app = simpleapp_tk(root)

	logging.info("Starting GUI Application")
	logging.info("Going in Event Loop")

	# Start the main loop
	root.mainloop()

	# Exit from mainloop
	logging.info("Exting from main loop")

	# Initiate Cleanup for unused files
	logging.info("Cleanup started")
	ut.cleanup("../csv_data", ".csv")
	ut.cleanup("../output_graphs", ".png")

# Call Main
if __name__ == "__main__":
	main()
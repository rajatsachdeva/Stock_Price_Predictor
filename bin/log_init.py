#!/Users/rohanrajat/anaconda/bin/python

import logging
import os.path

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)s()] - %(message)s'

def initialize_logger(output_dir, enable_console_output=True):
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	 
	 # If True then enable console logging
	if enable_console_output:
		# create console handler and set level to info
		handler 	= logging.StreamHandler()
		handler.setLevel(logging.INFO)
		formatter 	= logging.Formatter(FORMAT)
		handler.setFormatter(formatter)
		logger.addHandler(handler)
 
	# create error file handler and set level to error
	handler 		= logging.FileHandler(os.path.join(output_dir, "error.log"),"w", encoding=None, delay="true")
	handler.setLevel(logging.ERROR)
	formatter 		= logging.Formatter(FORMAT)
	handler.setFormatter(formatter)
	logger.addHandler(handler)
 
	# create debug file handler and set level to debug
	handler 		= logging.FileHandler(os.path.join(output_dir, "all.log"),"w")
	handler.setLevel(logging.DEBUG)
	formatter 		= logging.Formatter(FORMAT)
	handler.setFormatter(formatter)
	logger.addHandler(handler)
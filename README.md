# Stock_Price_Predictor

Usage for the program:
Save Your twitter access keys/consumer key in a file name auth.txt in directory ../secret/ relative from execution directory
in following format:

*** auth.txt ***

access_token=XXXXXXX

access_token_secret=XXXXXXXX

consumer_key=XXXXXXXXX

consumer_secret=XXXXXXXXXX

Sample Output for GUI:
  $ ./launch_gui.py
  
  Using TensorFlow backend. 
  
  Starting Program...
  
  Initializing...
  
  Starting GUI Application
  
  Going in Event Loop
  

![1](screen_grabs/first.jpg?raw=true)

Enter some stock symbol like GOOG, AAPL etc.

![2](screen_grabs/second.png?raw=true)

Result will look like this :

![3](screen_grabs/third.png?raw=true)

Sample Output for CLI:
$ ./main.py 
Using TensorFlow backend.
Starting Stock Price Prediction Program...

Enter (y/n)> y

Enter Stock Symbol (Like GOOG, AAPL etc.): AAPL

Enter number of days for which data is to fetched: 40

**** RESULT *****

Postive Tweets: 22

Negative Tweets: 4

 ** Prediction **

Current price: 156.6

RBF: 148.51054832412675

KERAS: 155.87838745117188

Enter (y/n)> n

Exiting from program...

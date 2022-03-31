import snscrape.modules.twitter as sntwitter #library used for scraping tweets
import pandas #library used for dataframe type
from textblob import TextBlob #library used for sentiment analysis
import yfinance as yf #library used for stock price info
import sys
import csv

def main(input1, input2a, input3a, input2b, input3b):
	tweetSent = scrapeTweets(input1, input2a, input3a) #returns list of input, sentiment and # of tweets
	##stockInfo = scrapePrices(input1, input2b, input3b) #returns % change of stock price
	stockInfo = 'seeChart' #Use if using a crypto or some other thing that wouldn't have a chart with yahoo finance
	return(tweetSent,stockInfo)
	
def scrapeTweets(tick, startDate, endDate):
	# Creating list to append tweet data to
	tweets_list2 = []
	sent = 0
	tot = 0
	userNames = [] #list for usernames tweeting about the certain stock
	unique = {} #unique dictionary with user:#tweets in the time period
	uniqueSent = {}
	# Using TwitterSearchScraper to scrape data and append tweets to list
	# clean inputs	
	#cleanTick = '$'+tick
	cleanTick = tick #Another thing that can be customized based off what you want (tags or not)
	#if '_' in tick: #if you want spaces
	#	cleanTick = tick.replace('_',' ')
	inputString = cleanTick + ' ' + "since:" + startDate + " " + "until:" + endDate
	print(inputString)
	unumber = 0
	for i,tweet in enumerate(sntwitter.TwitterSearchScraper(inputString).get_items()):
		if tot%100 == 0:
			print("tweets scraped: ",tot)		
		indivS = TextBlob(tweet.content).sentiment.polarity
		tot+=1
		#if unumber>X: #if you want to limit number of users scraped
			#break
		tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username, indivS])
		sent+=indivS
		userNames.append(tweet.user.username)
		if tweet.user.username not in uniqueSent:
			uniqueSent[tweet.user.username] = float(indivS)
			unumber+=1
			#print('not in')
		else:
			uniqueSent[tweet.user.username]+=float(indivS)
	
	# Average sentiment
	if tot != 0:
		sent = sent/tot
	else:
		sent = 0
	# Creating a dataframe from the tweets list above
	tweets_df2 = pandas.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'sentitment'])
	#print("\nAVERAGE SENTIMENT: ",sent, "of", tot, "tweets") #for viewing in terminal
	uniqueList = list(set(userNames)) # no duplicates
	for u in uniqueList: #add users to the unique dictionary with the number of tweets associated w/ their account
		count = userNames.count(u)
		unique[u] = count
	tempUS = uniqueSent
	#print(uniqueSent)
	for u in uniqueSent: #sentiment for accounts' tweets
		tempUS[u] = tempUS[u]/userNames.count(u)
	uniqueSent = tempUS
	userInfoList = []
	for i in uniqueList:
		userInfoList.append([i,unique[i],uniqueSent[i]])
	return(([tot,sent,tweets_list2,userInfoList,uniqueList])) #sends to main function

def scrapePrices(tick, startDate, endDate):
	# define the ticker symbol
	tickerSymbol = tick

	# get data on this ticker
	tickerData = yf.Ticker(tickerSymbol)

	# get the historical prices for this ticker
	tickerDf = tickerData.history(period='1d', start=startDate, end=endDate)
	tickerDf.Open

	# see your data (pandas DF to list)
	ez = tickerDf.Open.to_numpy()
	try: #error handling for if stock prices cannot be found 	
		percChange = str(round((((ez[-1]-ez[0])/ez[0])*100),3))+'%'
	except:
		None	
	print('%Change over time period:\n',percChange) #for viewing in terminal
	return(percChange) #sends to main function

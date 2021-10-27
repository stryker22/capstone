#!/usr/bin/env/ python3

import snscrape.modules.twitter as sntwitter #library used for scraping tweets
import pandas #library used for dataframe type
from textblob import TextBlob #library used for sentiment analysis
import yfinance as yf #library used for stock price info
import sys
import csv

def main(input1, input2, input3, input3b, input4):
	tweetSent = scrapeTweets(input1, input2, input3, input4) #returns list of input, sentiment and # of tweets
	stockInfo = scrapePrices(input1, input2, input3b) #returns % change of stock price
	with open('results.csv','a',newline='') as results: #writes data to .csv file for further analysis
		writer = csv.writer(results)
		writer.writerow([tweetSent[0],tweetSent[1],tweetSent[2],stockInfo])	

def scrapeTweets(tick, startDate, endDate, limit):
	# Creating list to append tweet data to
	tweets_list2 = []
	sent = 0
	tot = 0

	# Using TwitterSearchScraper to scrape data and append tweets to list
	# clean inputs	
	cleanTick = '$'+tick
	inputString = cleanTick + ' ' + "since:" + startDate + " " + "until:" + endDate
	print(inputString)
	for i,tweet in enumerate(sntwitter.TwitterSearchScraper(inputString).get_items()):
    		indivS = TextBlob(tweet.content).sentiment.polarity
    		tot+=1
    		if i>1000:
        		break
    		tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username, indivS])
    		sent+=indivS
	
	# Average sentiment
	if tot != 0:
		sent = sent/tot
	else:
		sent = 0
	# Creating a dataframe from the tweets list above
	tweets_df2 = pandas.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'sentitment'])
	print("\nAVERAGE SENTIMENT: ",sent, "of", tot, "tweets") #for viewing in terminal
	return([inputString,tot,sent]) #sends to main function

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
	print(percChange) #for viewing in terminal
	return(percChange) #sends to main function

#EXAMPLE COMMAND:
#main("NRG",'2020-01-21','2020-01-28','2020-02-05','y')
#this will return the average sentiment of tweets with $NRG (NRG Energy)
#over the time period 21JAN2021-28JAN2021, and then the stock percent
#change in price from 21JAN2021-05FEB2021




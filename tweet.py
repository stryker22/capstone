#!/usr/bin/env python3

import snscrape.modules.twitter as sntwitter
import pandas
from textblob import TextBlob
import yfinance as yf
import sys
import csv

def main(input1, input2, input3, input3b, input4):
	#GUI
	'''input1 = input("What ticker do you want to scrape? (ex: WISH) ")
	input2 = input("Beginning time range (ex: 2021-01-30): ")
	input3 = input("Ending time range: ")
	input4 = input("Limit number of results? (y/n) ")'''
	#input1 = 'WISH'
	#input2 = '2021-01-01'
	#input3 = '2021-02-01'
	#input4 = 'y'
	tweetSent = scrapeTweets(input1, input2, input3, input4) #returns list of input, sentiment and #of twetts
	stockInfo = scrapePrices(input1, input2, input3b)
	#stockInfo['Tweet Sentiment'] = tweetSent
	with open('results.csv','a',newline='') as results:
		writer = csv.writer(results)
		writer.writerow([tweetSent[0],tweetSent[1],tweetSent[2],stockInfo])
	#print('this is it boys\n')
	#print(stockInfo)	

def scrapeTweets(tick, startDate, endDate, limit):
	# Creating list to append tweet data to
	tweets_list2 = []
	sent = 0
	tot = 0

	# Using TwitterSearchScraper to scrape data and append tweets to list
	#clean inputs	
	cleanTick = '$'+tick
	inputString = cleanTick + ' ' + "since:" + startDate + " " + "until:" + endDate
	print(inputString)
	for i,tweet in enumerate(sntwitter.TwitterSearchScraper(inputString).get_items()):
    		indivS = TextBlob(tweet.content).sentiment.polarity
    		tot+=1
    		if i>1000:
        		break
    		tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username, indivS])
    		#blob = TextBlob(tweet.content)
    		#if sent > 0 or sent > 0:
    		sent+=indivS
	# Creating a dataframe from the tweets list above
	#Average sentiment
	sent = sent/tot

	tweets_df2 = pandas.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'sentitment'])
	#compression_opts = dict(method='zip',archive_name='outLongN.csv') 
	#tweets_df2.to_csv('testLongN.zip', index=False,compression=compression_opts)
	#print(tweets_df2)
	print("\nAVERAGE SENTIMENT: ",sent, "of", tot, "tweets")
	return([inputString,tot,sent])

def scrapePrices(tick, startDate, endDate):
	#define the ticker symbol
	tickerSymbol = tick

	#get data on this ticker
	tickerData = yf.Ticker(tickerSymbol)

	#get the historical prices for this ticker
	tickerDf = tickerData.history(period='1d', start=startDate, end=endDate)
	tickerDf.Open

	#see your data
	#print(tickerDf.Open)
	ez = tickerDf.Open.to_numpy()
	percChange = str(round((((ez[-1]-ez[0])/ez[0])*100),3))+'%'
	#print(tickerDf.Open.to_numpy())
	print(percChange)
	return(percChange)
main("WISH",'2021-01-21','2021-02-01','2021-02-08',"y")
main("WISH",'2021-02-20','2021-03-03','2021-03-10',"y")
main("WISH",'2021-03-22','2021-04-02','2021-04-09',"y")
main("WISH",'2021-04-21','2021-05-02','2021-05-09',"y")
main("WISH",'2021-05-21','2021-06-01','2021-06-08',"y")
main("WISH",'2021-06-20','2021-07-01','2021-07-08',"y")
main("WISH",'2021-07-20','2021-07-31','2021-08-07',"y")
main("WISH",'2021-08-19','2021-08-30','2021-09-06',"y")
main("SPY",'2021-01-21','2021-02-01','2021-02-08',"y")
main("SPY",'2021-02-20','2021-03-03','2021-03-10',"y")
main("SPY",'2021-03-22','2021-04-02','2021-04-09',"y")
main("SPY",'2021-04-21','2021-05-02','2021-05-09',"y")
main("SPY",'2021-05-21','2021-06-01','2021-06-08',"y")
main("SPY",'2021-06-20','2021-07-01','2021-07-08',"y")
main("SPY",'2021-07-20','2021-07-31','2021-08-07',"y")
main("SPY",'2021-08-19','2021-08-30','2021-09-06',"y")
main("F",'2021-01-21','2021-02-01','2021-02-08',"y")
main("F",'2021-02-20','2021-03-03','2021-03-10',"y")
main("F",'2021-03-22','2021-04-02','2021-04-09',"y")
main("F",'2021-04-21','2021-05-02','2021-05-09',"y")
main("F",'2021-05-21','2021-06-01','2021-06-08',"y")
main("F",'2021-06-20','2021-07-01','2021-07-08',"y")
main("F",'2021-07-20','2021-07-31','2021-08-07',"y")
main("F",'2021-08-19','2021-08-30','2021-09-06',"y")
main("GE",'2021-01-21','2021-02-01','2021-02-08',"y")
main("GE",'2021-02-20','2021-03-03','2021-03-10',"y")
main("GE",'2021-03-22','2021-04-02','2021-04-09',"y")
main("GE",'2021-04-21','2021-05-02','2021-05-09',"y")
main("GE",'2021-05-21','2021-06-01','2021-06-08',"y")
main("GE",'2021-06-20','2021-07-01','2021-07-08',"y")
main("GE",'2021-07-20','2021-07-31','2021-08-07',"y")
main("GE",'2021-08-19','2021-08-30','2021-09-06',"y")
main("VZ",'2021-01-21','2021-02-01','2021-02-08',"y")
main("VZ",'2021-02-20','2021-03-03','2021-03-10',"y")
main("VZ",'2021-03-22','2021-04-02','2021-04-09',"y")
main("VZ",'2021-04-21','2021-05-02','2021-05-09',"y")
main("VZ",'2021-05-21','2021-06-01','2021-06-08',"y")
main("VZ",'2021-06-20','2021-07-01','2021-07-08',"y")
main("VZ",'2021-07-20','2021-07-31','2021-08-07',"y")
main("VZ",'2021-08-19','2021-08-30','2021-09-06',"y")
main("DIS",'2021-01-21','2021-02-01','2021-02-08',"y")
main("DIS",'2021-02-20','2021-03-03','2021-03-10',"y")
main("DIS",'2021-03-22','2021-04-02','2021-04-09',"y")
main("DIS",'2021-04-21','2021-05-02','2021-05-09',"y")
main("DIS",'2021-05-21','2021-06-01','2021-06-08',"y")
main("DIS",'2021-06-20','2021-07-01','2021-07-08',"y")
main("DIS",'2021-07-20','2021-07-31','2021-08-07',"y")
main("DIS",'2021-08-19','2021-08-30','2021-09-06',"y")
main("HD",'2021-01-21','2021-02-01','2021-02-08',"y")
main("HD",'2021-02-20','2021-03-03','2021-03-10',"y")
main("HD",'2021-03-22','2021-04-02','2021-04-09',"y")
main("HD",'2021-04-21','2021-05-02','2021-05-09',"y")
main("HD",'2021-05-21','2021-06-01','2021-06-08',"y")
main("HD",'2021-06-20','2021-07-01','2021-07-08',"y")
main("HD",'2021-07-20','2021-07-31','2021-08-07',"y")
main("HD",'2021-08-19','2021-08-30','2021-09-06',"y")
main("NKE",'2021-01-21','2021-02-01','2021-02-08',"y")
main("NKE",'2021-02-20','2021-03-03','2021-03-10',"y")
main("NKE",'2021-03-22','2021-04-02','2021-04-09',"y")
main("NKE",'2021-04-21','2021-05-02','2021-05-09',"y")
main("NKE",'2021-05-21','2021-06-01','2021-06-08',"y")
main("NKE",'2021-06-20','2021-07-01','2021-07-08',"y")
main("NKE",'2021-07-20','2021-07-31','2021-08-07',"y")
main("NKE",'2021-08-19','2021-08-30','2021-09-06',"y")
main("SBUX",'2021-01-21','2021-02-01','2021-02-08',"y")
main("SBUX",'2021-02-20','2021-03-03','2021-03-10',"y")
main("SBUX",'2021-03-22','2021-04-02','2021-04-09',"y")
main("SBUX",'2021-04-21','2021-05-02','2021-05-09',"y")
main("SBUX",'2021-05-21','2021-06-01','2021-06-08',"y")
main("SBUX",'2021-06-20','2021-07-01','2021-07-08',"y")
main("SBUX",'2021-07-20','2021-07-31','2021-08-07',"y")
main("SBUX",'2021-08-19','2021-08-30','2021-09-06',"y")

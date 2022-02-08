import sys
import tweet
import csv 
import botOrNot22
import locationData

def main():
    
    if len(sys.argv) == 1:
        print('USAGE:\n-s [stock]\n-sd [begin date,end date]\n-t [tweet begin, end date]\n-b (for bot analysis)\n-l (for location analysis)\n\nEXAMPLE: \npython3 bigDaddy.py -s GME -sd 2020-01-30,2020-02-11 -t 2020-01-30,2020-02-03 -b -l')
    
    elif len(sys.argv) < 7:
        print('stock, stock dates, and tweet dates required')
    
    # Scrape tweets and prices
    elif len(sys.argv)==7:
        twitterAndStockData(sys.argv[2],sys.argv[4],sys.argv[6])
        with open('betaTesting.csv','a',newline='') as results:
                writer = csv.writer(results)
                writer.writerow([info[0][0],info[0][1],info[1]]) #write total# of tweets, avg sentiment, and % change to csv
                for i in info[0][3]: #write number of tweets and sentiment attributed to each user
                        writer.writerow(i)          

    # Scrape bot info on accounts
    elif len(sys.argv)>7 and sys.argv.count('-b')==1 and sys.argv.count('-l')==0:
        print('botOnly')
        info = twitterAndStockData(sys.argv[2],sys.argv[4],sys.argv[6])
        print('accounts to analyze:\n',info[0][4])
        botInfo = bot(info[0][4])
        with open('betaTesting.csv','a',newline='') as results:
                writer = csv.writer(results)
                writer.writerow([info[0][0],info[0][1],info[1]]) #write total# of tweets, avg sentiment, and % change to csv
                for i in info[0][3]: #write number of tweets and sentiment attributed to each user
                        writer.writerow(i)          
                for iKey in botInfo: #writer bot analysis for each user 
                        writer.writerow([iKey,botInfo[iKey]])

    # Scrape location info on accounts
    elif len(sys.argv)>7 and sys.argv.count('-l')==1 and sys.argv.count('-b')==0:
        print('locOnly')
        info = twitterAndStockData(sys.argv[2],sys.argv[4],sys.argv[6])
        print('accounts to analyze:\n',info[0][4])
        locInfo = loc(info[0][4])
        with open('betaTesting.csv','a',newline='') as results:
                writer = csv.writer(results)
                writer.writerow([info[0][0],info[0][1],info[1]]) #write total# of tweets, avg sentiment, and % change to csv
                for i in info[0][3]: #write number of tweets and sentiment attributed to each user
                        writer.writerow(i)          
                for iiKey in locInfo: #write location analysis for each user
                        writer.writerow([iiKey,locInfo[iiKey]])

    # Scrape location info AND bot info on accounts
    elif len(sys.argv)>8 and sys.argv.count('-l')==1 and sys.argv.count('-b')==1:
        print('locAndBot')
        info = twitterAndStockData(sys.argv[2],sys.argv[4],sys.argv[6])
        print('accounts to analyze:\n',info[0][4])
        print('\n',info)
        botInfo = bot(info[0][4])
        locInfo = loc(info[0][4])
        print('results:\n')
        print(botInfo,locInfo)
        with open('betaTesting.csv','a',newline='') as results:
                writer = csv.writer(results)
                writer.writerow([info[0][0],info[0][1],info[1]]) #write total# of tweets, avg sentiment, and % change to csv
                for i in info[0][3]: #write number of tweets and sentiment attributed to each user
                        writer.writerow(i)          
                for iKey in botInfo: #writer bot analysis for each user 
                        writer.writerow([iKey,botInfo[iKey]])
                for iiKey in locInfo: #write location analysis for each user
                        writer.writerow([iiKey,locInfo[iiKey]])

def twitterAndStockData(stock,Sdates,Tdates): #returns list with #tweets, sentiment, tweets w/ info, accounts w/ info, accounts, %change
    tweetDates = Tdates.split(',')
    stockDates = Sdates.split(',')
    info = tweet.main(stock,tweetDates[0],tweetDates[1],stockDates[0],stockDates[1])
    return(info)

def bot(accounts): # Returns dictionary with username:botScore
    return(botOrNot22.botDaddy(accounts))

def loc(accounts): # Returns dictionary with username:location
    return(locationData.main(accounts))




if __name__ == '__main__':
    main()


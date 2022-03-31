import botometer
import statistics #standard deviation
#general use guidance from https://medium.com/analytics-vidhya/twitter-sentiment-analysis-botometer-part-2-aecdbbbada30
def botDaddy(users):
	masterUsers = {}
	rapidapi_key = ""
	twitter_app_auth = {'consumer_key': '','consumer_secret': '','access_token': '','access_token_secret': ''}
	bom = botometer.Botometer(wait_on_ratelimit=True,rapidapi_key=rapidapi_key,**twitter_app_auth)
	print('analyzing for bots...\n')
	c = 0 #counter
	total = 0 #for calculating average
	totalN = 0 #total number of accounts
	capVals = [] #list to return for std dev calculation
	for screen_name, result in bom.check_accounts_in(users):
		try:
			#print(screen_name, c, 'of', len(users),'\n')
			if c%100 == 0:
				print("accounts analyzed: ",c)
			masterUsers[screen_name] = result['cap']['english'],result['raw_scores']['english']['overall'] #master dict key pair added
			total+=float(result['cap']['english'])
			totalN+=1
			capVals.append(float(result['cap']['english']))			
		except:
			None
		c+=1
	averageCAP = total/totalN #ease
	stddev = statistics.pstdev(capVals) #ease
	masterUsers['0']=[averageCAP,stddev] #ease
	return(masterUsers)

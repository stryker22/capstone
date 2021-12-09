import botometer
import csv

users = [] #list with usernames
nums = {} #dict with 'username':# of tweets for accounts wanting to be analyzed
def botDaddy(users,nums):
	
	masterUsers = {} #dictionary with user:'botScore,#tweets'
	rapidapi_key = ""
	twitter_app_auth = {'consumer_key': '','consumer_secret': '','access_token': '','access_token_secret': ''}
	bom = botometer.Botometer(wait_on_ratelimit=True,rapidapi_key=rapidapi_key,**twitter_app_auth)
	for screen_name, result in bom.check_accounts_in(users):
		try:
			masterUsers[screen_name] = (result['cap']['english'],result['raw_scores']['english']['overall'],nums[screen_name])
			print(screen_name,result['cap']['english'],result['raw_scores']['english']['overall'],nums[screen_name])
			with open('analysisSQUID.csv','a',newline='') as results:
				writer = csv.writer(results)
				writer.writerow([screen_name,result['cap']['english'],result['raw_scores']['english']['overall'],nums[screen_name]])
		#results.close()
		except:
			None
	return(masterUsers)

botDaddy(users,nums)

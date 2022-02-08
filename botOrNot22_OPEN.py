import botometer

def botDaddy(users):
	masterUsers = {}
	rapidapi_key = ""
	twitter_app_auth = {'consumer_key': '','consumer_secret': '','access_token': '','access_token_secret': ''}
	bom = botometer.Botometer(wait_on_ratelimit=True,rapidapi_key=rapidapi_key,**twitter_app_auth)
	print('analyzing:\n')
	for screen_name, result in bom.check_accounts_in(users):
		try:
			print(screen_name,'\n')
			masterUsers[screen_name] = result['cap']['english'],result['raw_scores']['english']['overall']
			
		except:
			None
	return(masterUsers)

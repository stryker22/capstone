import os
from requests_oauthlib import OAuth1Session #authenticate
import json
import csv
import time #Twitter rules...

def main(accounts):
    # Add your API key here
    consumer_key = ""
    # Add your API secret key here
    consumer_secret = ""

    fields = "created_at,description,pinned_tweet_id" #change based on what you want
	
	#FOLLOWING IS FROM 
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)
    
    # Get authorization https://docs.tweepy.org/en/stable/api.html
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print("Please go here and authorize: %s" % authorization_url)
    verifier = input("Paste the PIN here: ")
    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    
    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]
    
    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    masterDict = {}
    locationList = []
    c = 0
    print("analyzing locations...will take 15 minute break after every 300 accounts...")
    for i in accounts:
        params = {"usernames": i, "user.fields": 'location'} #specify what we wanna scrape
        response = oauth.get("https://api.twitter.com/labs/2/users/by?", params=params)
        #print(response)
        #print("Body: %s" % response.text, c)
        if "Too Many Requests" in response.text: #Need this or it will just keep going
            print("Accounts scraped: ",c," Too many! sleeping now zzz")
            accounts.append(i)
            time.sleep(910)
            continue
        try: #convert json to dictionary
                jso = json.loads(response.text)
        except:
                None
        try:
                x = jso['data'][0]["location"],jso['data'][0]["username"]
                masterDict[jso['data'][0]["username"]]=jso['data'][0]["location"]
                locationList.append(jso['data'][0]["location"])
        except:
        	None
        c+=1
    for i in accounts: #when location isn't set on account
        if i not in masterDict.keys():
                masterDict[i] = 'no location'
    masterDict["0"] = locationList #for easy writing to file for word cloud
    return(masterDict)


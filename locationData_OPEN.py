import os
from requests_oauthlib import OAuth1Session
import json
import csv

def main(accounts):
    # Add your API key here
    consumer_key = ""
    # Add your API secret key here
    consumer_secret = ""
    #with open('segmented.txt') as st: #txt file with 100 item lists of desired accounts analyzed
        #lines=st.readlines()
	

    fields = "created_at,description,pinned_tweet_id"
    #params = {"usernames": un, "user.fields": 'location'}

    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    print("Got OAuth token: %s" % resource_owner_key)
    
    # Get authorization
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
    for i in accounts:
        params = {"usernames": i, "user.fields": 'location'}
        response = oauth.get("https://api.twitter.com/labs/2/users/by?", params=params)
        #print(response)
        #print("Body: %s" % response.text)
        jso = json.loads(response.text)
        try:
                x = jso['data'][0]["location"],jso['data'][0]["username"]
                masterDict[jso['data'][0]["username"]]=jso['data'][0]["location"]
        except:
        	None
    for i in accounts:
        if i not in masterDict.keys():
                masterDict[i] = 'no location'
    return(masterDict)
    '''for l in lines:
	    string = l.strip()
	    string=string.replace("'",'')
	    params = params = {"usernames": string, "user.fields": 'location'}
	    response = oauth.get("https://api.twitter.com/labs/2/users/by?", params=params)
	    #print(response)
	    #print("Response status: %s" % response.status_code)
	    #print("Body: %s" % response.text)
	    jso = json.loads(response.text)
	    c = 0
	    while c<100:
	        try:
	            print(jso['data'][c]["location"],jso['data'][c]["username"])
	            with open('SQUIDlocation.csv','a',newline='') as results:
	                writer = csv.writer(results)
	                writer.writerow([jso['data'][c]["location"],jso['data'][c]["username"]])
	            results.close()
	        except:
	            None
	        c+=1'''

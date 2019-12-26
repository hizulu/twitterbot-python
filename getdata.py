import tweepy
import json

ACCESS_TOKEN = "1177856298-9FJ7Yw7E8cshcR2gWEJKUN7IHxGhp3IVaaRKlmG"
ACCESS_TOKEN_SECRET = "KUPi11ZUtlgDigIVdriG8JMp9NtPKzoSC6BYrNFHS9cvr"
CONSOMER_KEY = "jdmH1Ncnc4vcKQhrTY1C7NUEQ"
CONSUMER_KEY_SECRET = "TYZUCdiyUEhbPyBRxQqFGHGNS5gRFm8MJSUF4VAHzZTWU970YJ"

def connectToTwitterOAuth():
    auth = tweepy.OAuthHandler(CONSOMER_KEY, CONSUMER_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api


api = connectToTwitterOAuth()
for item in tweepy.Cursor(api.search, q="garuda indonesia", since="2019-11-01", until="2019-12-24", tweet_mode="extended").items(3):
    print(item)
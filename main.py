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
for friend in tweepy.Cursor(api.friends).items(5):
    detail = friend._json
    print("Processing '{}'".format(detail['screen_name']))
    data = {
        'name': detail['name'],
        'username': detail['screen_name'],
        'descriptiion': detail['description']
    }
    tweets = []
    # get tweet from the user
    for item in api.user_timeline(detail['screen_name'], count=5):
        tweet = item._json
        tweets.append({
            'text': tweet['text'],
            'created_at': tweet['created_at'],
            'real': tweet
        })

    data['tweets'] = tweets
    file = open(detail['screen_name'] + '.json', 'w')
    file.write(json.dumps(data, indent=1))
    file.close()

    # print(json.dumps(item._json, indent=1))
# public_tweet = api.home_timeline()
# for tweet in public_tweet:
#     print(tweet.text)

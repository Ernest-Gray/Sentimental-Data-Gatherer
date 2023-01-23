import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

bearer_token = "AAAAAAAAAAAAAAAAAAAAANBhlQEAAAAAGYIXOABKJyW0Z9VKIPZwrLw9MEs%3Dc9xchzTR5PEKOTxEQJs4paRQbSbcBrW8AwCrNGs7lyC6NXuUlG"

auth = tweepy.OAuth2BearerHandler(bearer_token)


api = tweepy.Client(auth)

results = api.search(q='Elon Musk')
for tweet in results:
    print(tweet.text)
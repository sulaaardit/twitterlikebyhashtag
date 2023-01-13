import tweepy
import time


# Enter your API keys and access tokens here
consumer_key = "consumer_key"
consumer_secret = "consumer_secret"
access_token = "access_token"
access_token_secret = "access_token_secret"

# Authenticate with the Twitter API
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Search for tweets with a specific hashtag
hashtag = "#yourhashtag"

# Define the maximum number of tweets to like per 15 minutes
max_tweets_per_15_minutes = 80

# Use the Cursor to paginate through the tweets
start_time = time.time()
liked_tweet_count = 0
for tweet in tweepy.Cursor(api.search_tweets, q=hashtag).items():
    # Check if the maximum number of tweets per 15 minutes has been reached
    if liked_tweet_count >= max_tweets_per_15_minutes:
        elapsed_time = time.time() - start_time
        if elapsed_time < 900:
            time.sleep(900 - elapsed_time)
        start_time = time.time()
        liked_tweet_count = 0
    status = api.get_status(tweet.id)
    if not status.favorited:
        try:
            api.create_favorite(tweet.id)
            liked_tweet_count += 1
            print(f"Liked tweet: {tweet.user.screen_name}")
        except tweepy.TweepError as e:
            print(e.reason)

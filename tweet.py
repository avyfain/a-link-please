import os
import random
import tweepy
import redis

CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

r = redis.from_url(os.environ.get("REDIS_URL"))

phrases = ['Here you go',
           'A link coming right up',
           'Done',
           "I know what you're thinking. Zelda was the princess though"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
twitter = tweepy.API(auth)

def tweet_back(tweet):
    username = tweet.user.screen_name

    img = 'img/{}.png'.format(random.choice(range(10)))
    message = '{}, @{}!'.format(random.choice(phrases), username)

    print("Replying to {}'s tweet with ID {}".format(username, tweet.id))
    twitter.update_with_media(filename=img, status=message, in_reply_to_status_id=tweet.id)

if __name__ == '__main__':
    tweets = twitter.search('"link please"')
    random_tweet = next((tweet for tweet in tweets if not tweet.retweeted), None)

    tweet_back(random_tweet)

    replies = twitter.search('@alinkplease link please', since_id=r.get('last'))
    if replies:
        r.set('last', replies[0].id)
    for tweet in replies:
        tweet_back(tweet)
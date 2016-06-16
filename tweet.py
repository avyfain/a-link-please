import os
import random
import tweepy

CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

phrases = ['Here you go',
           'A link coming right up',
           'Done',
           "I know what you're thinking. Zelda was the princess though"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
twitter = tweepy.API(auth)


if __name__ == '__main__':
    random_tweet = twitter.search('"link please"')[0]
    username = random_tweet.user.screen_name

    img = 'img/{}.png'.format(random.choice(range(10)))
    message = '{}, @{}!'.format(random.choice(phrases), username)

    print("Replying to {}'s tweet with ID {}".format(username, random_tweet.id))

    twitter.update_with_media(filename=img, status=message, in_reply_to_status_id=random_tweet.id)

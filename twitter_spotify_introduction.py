import sys
import datetime
from twitter import *
from spotipy import *
from spotipy.oauth2 import SpotifyClientCredentials

from config import *
from util import *

config_txt = 'config.txt'
with open(config_txt, 'r') as f:
    twitter_token, twitter_token_secret, spotify_id, spotify_secret = (l.strip() for l in f.readlines())

t = Twitter(
    auth=OAuth(
        twitter_token,
        twitter_token_secret,
        consumer_key,
        consumer_secret,
    )
)

# search parent
tweets = t.statuses.user_timeline(screen_name='kenttcrane', count=100)
parent = None

for tweet in tweets:
    if not tweet['entities']['urls']:
        continue
    if 'spotify' not in tweet['entities']['urls'][0]['expanded_url']:
        continue
    root_id = root_tweet_id(t, tweet)
    # if root_id == SPOTIFY_ROOT_TWEET_ID:
    if root_id == SPOTIFY_ROOT_TWEET_ID:
        parent = tweet
        break

# parent = t.statuses.show(_id=TEST_TWEET_ID)

if parent == None:
    print('No parent.')
    sys.exit(1)

print('parent: ')
show_dict(parent)

# spotify setup
ccm = SpotifyClientCredentials(client_id=spotify_id, client_secret=spotify_secret)
spotify = Spotify(client_credentials_manager=ccm, language='ja')

# get track info
while True:
    url = input('spotify track url: ')
    try:
        info = spotify.track(url)
        break
    except:
        print('invalid input')
        print()
        pass

# check track information
# show_dict(info)
while True:
    print(f"title: {info['name']}")
    title = input('If the title is correct, press enter. If not, type the correct title.')
    if title == '':
        title = info['name']

    print(f"artist: {info['artists'][0]['name']}")
    artist = input('If the artist is correct, press enter. If not, type the correct artist.')
    if artist == '':
        artist = info['artists'][0]['name']

    dt = datetime.datetime.now()
    month = dt.month
    day = dt.day - (1 if dt.hour < 5 else 0)
    date_str = str(month) + '/' + str(day)
    
    multi_today = (input('multiple introduction today? (y/n): ') == 'y')
    if multi_today:
        num = input('input the tweet number: ')
        date_str += ' (' + num + ')'

    # check tweet text
    text = date_str + '\n' + title + ' - ' + artist + '\n' + url
    while True:
        print(f'text: "{text}"')
        ans = input('OK? (y/n)')
        if ans in ('y', 'n'):
            break
        else:
            print('invalid answer')
    if ans == 'y':
        break
    else:
        print('input the information again.')
    
#tweet
print('-'*30)
print(text)
print('-'*30)
t.statuses.update(status=text, in_reply_to_status_id=parent['id'])
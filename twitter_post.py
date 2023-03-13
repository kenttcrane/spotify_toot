from twitter import *

from config import *
from util import *

config_txt = 'config.txt'
with open(config_txt, 'r') as f:
    token, token_secret = [l.strip() for l in f.readlines()][0:2]

t = Twitter(
    auth=OAuth(
        token,
        token_secret,
        consumer_key,
        consumer_secret,
    )
)

t.statuses.update(status='うゆ\n' + "https://www.lovelive-anime.jp/", in_reply_to_status_id=TEST_TWEET_ID)
from twitter import *

from config import *
from util import *

config_txt = 'config.txt'
with open(config_txt, 'r') as f:
    token, token_secret = (l.strip() for l in f.readlines())

t = Twitter(
    auth=OAuth(
        token,
        token_secret,
        consumer_key,
        consumer_secret,
    )
)

a = t.statuses.show(_id=1614922484863864832)
print(a)

# a = t.statuses.home_timeline(count=50)
a = t.statuses.user_timeline(screen_name='kenttcrane', count=10)
for tweet in a:
    show_dict(tweet)
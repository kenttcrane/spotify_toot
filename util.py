import numpy
import twitter


root = {}

def root_tweet_id(t, tweet):
    id = tweet['id']
    if id in root:
        return root[id]

    ids = numpy.array([id])
    while tweet['in_reply_to_status_id'] != None:
        parent_id = tweet['in_reply_to_status_id']
        print(parent_id)
        ids = numpy.append(ids, parent_id)
        tweet = t.statuses.show(_id=parent_id)
    
    root_id = tweet['id']
    for child_id in ids:
        root[child_id] = root_id

    return root_id

def show_dict(d):
    for key in d:
        print(f'{key}: {d[key]}')
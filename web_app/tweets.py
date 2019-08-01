import tweepy
from decouple import config
from .models import db, Tweet, User
import basilica
import flask
from sklearn.linear_model import LogisticRegression
APP = flask.current_app
TWITTER_AUTH = tweepy.OAuthHandler(
    config('TWITTER_CONSUMER_KEY'),
    config('TWITTER_CONSUMER_SECRET'),
)
TWITTER_AUTH.set_access_token(
    config('TWITTER_ACCESS_TOKEN'),
    config('TWITTER_ACCESS_TOKEN_SECRET'), 
)

TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

def add_or_update_user(username):
    """Add or update user and tweets"""
    try:
        APP.logger.info(username)
        t_user = TWITTER.get_user(username)
        db_user = (
            User.query.get(t_user.id) or
            User(id=t_user.id, username=t_user.screen_name, name=t_user.name))
        db.session.add(db_user)
        APP.logger.info(db_user)
        last_tweet_id = \
            db_user.tweets.order_by(Tweet.id.desc()).first() or None
        last_tweet_id = last_tweet_id.id if last_tweet_id else None
        APP.logger.info(last_tweet_id)
        timeline = t_user.timeline(
            count=200, exclude_replies=True,
            include_rts=False, tweet_mode='extended',
            since_id=last_tweet_id)
        if timeline:
            timeline_text, tweet_id = zip(
                *[(t.full_text, t.id)for t in timeline])
            embeddings = BASILICA.embed_sentences(
                timeline_text,
                model='twitter',
            )
            tweet_list = list(zip(tweet_id, timeline_text, embeddings))
            tweet_objects = [Tweet(id=t[0], text=t[1][:500], embeddings=t[2])
                            for t in tweet_list]
            db_user.tweets.extend(tweet_objects)
    except Exception as e:
        APP.logger.info(f'Error processing {username}')
        APP.logger.info(e)
        raise e
    else:
        db.session.commit()

 
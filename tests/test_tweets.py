"""Tests for src/tweets."""

from src import settings
from src.utils import redis_cli
from src.tweets import stats
from src.tweets.stats import TOP_USERS_RKEY, HASHTAGS_STATS_RKEY, TWEETS_RKEY, TWEETS_COUNT_RKEY
from src.tweets.fetch import fetch_tweets


COUNT_TW_QUERY: str = '''select count(id) as count
from tweets;'''

COUNT_TW_BY_PHRASE: str = f'''{COUNT_TW_QUERY}
where text like "%{settings.PHRASE}%";
'''

UNIQ_TWEETS: str = f'''select count(distinct id) as count
from tweets;
'''


def test_tweets_count():
    assert stats.tweets_count() == 6


def test_top_hashtags():
    top_hashtags = stats.top_hashtags()

    assert top_hashtags[0]['tag'] == 'tag1'
    assert top_hashtags[0]['count'] == 6
    assert top_hashtags[1]['tag'] == 'tag2'
    assert top_hashtags[1]['count'] == 3
    assert top_hashtags[2]['tag'] == 'tag3'
    assert top_hashtags[2]['count'] == 2


def test_top_user():
    top_user = stats.top_users()

    assert top_user[0]['id'] == 1
    assert top_user[0]['count'] == 3
    assert top_user[1]['id'] == 2
    assert top_user[1]['count'] == 2
    assert top_user[2]['id'] == 3
    assert top_user[2]['count'] == 1


def test_fetch_tweets(engine):
    tweets_before_fetch = engine.execute(COUNT_TW_QUERY).first()['count']

    # make two calls to ensure no duplicates are being created
    fetch_tweets()
    fetch_tweets()

    tweets_created = engine.execute(COUNT_TW_QUERY).first()['count']
    tweets_with_phrase = engine.execute(COUNT_TW_QUERY).first()['count']
    uniq_tweets = engine.execute(UNIQ_TWEETS).first()['count']

    assert tweets_created - tweets_before_fetch <= settings.TWEETS_COUNT, 'Got extra tweets'
    assert tweets_created == uniq_tweets, 'Got duplicates'
    assert tweets_created == tweets_with_phrase, 'Some tweets without phrase'

    for key in (TOP_USERS_RKEY, HASHTAGS_STATS_RKEY, TWEETS_RKEY, TWEETS_COUNT_RKEY):
        assert redis_cli.exists(key), f'Missing key <{key}> in cache'

"""Periodically fetch recent tweets and store them to database."""

import time
from typing import Dict, List

import requests
import schedule
from sqlalchemy.dialects import postgresql

from src import settings
from src.utils import db_engine
from src.tweets import stats
from src.tweets import TwitType, UserType
from src.tweets.tables import tweets, users



def get_auth_token() -> str:
    """Returns Twitter oauth2 token"""

    token_request: requests.Response = requests.post(
        url='https://api.twitter.com/oauth2/token',
        data={'grant_type': 'client_credentials'},
        auth=(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET),
        headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'},
    )
    return token_request.json().get('access_token', '')


def get_tweets(
        phrase: str = settings.PHRASE, count: int = settings.TWEETS_COUNT
    ) -> List[dict]:
    """Returns list of <count> tweets queried by <phrase>."""
    token: str = get_auth_token()

    tweets_data_request: requests.Response = requests.get(
        url='https://api.twitter.com/1.1/search/tweets.json',
        headers={'Authorization': f'Bearer {token}', 'result_type': 'recent'},
        params={'q': phrase, 'count': count,}, #type: ignore
    )

    return tweets_data_request.json()['statuses']


def parse_hastags(twit: dict) -> List[str]:
    """Returns list of twitt's hastags"""
    return [ht['text'] for ht in twit['entities']['hashtags']]


def fetch_tweets():
    """Get tweets and store them to database."""
    new_tweets: list = get_tweets()

    if not new_tweets:
        return

    # use dict for users to avoid duplicates
    users_to_insert: Dict[int, UserType] = {}
    tweets_to_insert: List[TwitType] = []

    for twit in new_tweets:
        users_to_insert[twit['user']['id']] = {
            'id': twit['user']['id'],
            'screen_name': twit['user']['screen_name'],
        }

        tweets_to_insert.append(
            {
                'id': twit['id'],
                'text': twit['text'],
                'published_at': twit['created_at'],
                'user_id': twit['user']['id'],
                'hashtags': parse_hastags(twit),
            }
        )

    users_query: postgresql.Insert = postgresql.insert(users).values(
        list(users_to_insert.values())
    ).on_conflict_do_nothing(index_elements=['id'])

    tweets_query: postgresql.Insert = postgresql.insert(tweets).values(
        tweets_to_insert
    ).on_conflict_do_nothing(index_elements=['id'])

    with db_engine.begin() as connection:
        connection.execute(users_query)
        connection.execute(tweets_query)

        # update cache
        stats.new_tweets()
        stats.tweets_count()
        stats.top_hashtags()
        stats.top_users()


if __name__ == '__main__':
    schedule.every(settings.TIME_INTERVAL).minutes.do(fetch_tweets)

    while True:
        schedule.run_pending()
        time.sleep(1)

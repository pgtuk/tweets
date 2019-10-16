"""Queries and methods to gather basic tweets statistics."""

from typing import List
from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.sql import column
from sqlalchemy.sql.elements import BinaryExpression, ColumnClause, Label
from sqlalchemy.sql.selectable import Select, Alias

from src import settings
from src.utils import cache_result, db_engine

from src.tweets import HashtagStatType, UsersStatType, TwitType
from src.tweets.tables import tweets, users


TOP_HASHTAGS_LIMIT: int = 3
TOP_USERS_LIMIT: int = 3

TWEETS_RKEY: str = 'tweets'
HASHTAGS_STATS_RKEY: str = 'hashtags'
TOP_USERS_RKEY: str = 'top_users'
TWEETS_COUNT_RKEY: str = 'tweets_count'


@cache_result(TWEETS_RKEY)
def new_tweets() -> List[TwitType]:
    """Returns tweets added in last fetch session."""

    query: Select = select(
        [tweets]
    ).select_from(tweets.join(users)).where(
        _condition_recently_fetched_tweets(),
    )

    return [
        {
            'id': r.id,
            'user_id': r.user_id,
            'published_at': r.published_at.ctime(),
            'text': r.text,
            'hashtags': r.hashtags,
        }
        for r in db_engine.execute(query)
    ]


@cache_result(HASHTAGS_STATS_RKEY)
def top_hashtags() -> List[HashtagStatType]:
    """Returns top hashtags found in tweets."""

    unnested_tags_query: Alias = select(
        [func.unnest(tweets.c.hashtags).label('tag')]
    ).select_from(tweets).where(
        _condition_recently_fetched_tweets(),
    ).alias('t').as_scalar().alias('t')

    tags: ColumnClause = column('tag')
    tags_count: Label = func.count(tags).label('count')

    query: Select = select(
        [tags, tags_count]
    ).select_from(
        unnested_tags_query
    ).group_by(
        tags
    ).order_by(
        tags_count.desc()
    ).limit(TOP_HASHTAGS_LIMIT)

    return [dict(r) for r in db_engine.execute(query)]


@cache_result(TOP_USERS_RKEY)
def top_users() -> List[UsersStatType]:
    """Returns top 3 users that made max amount of tweets."""

    tw_count: Label = func.count(tweets.c.id).label('count')

    query: Select = select(
        [users.c.id, users.c.screen_name, tw_count]
    ).select_from(
        users.join(tweets)
    ).where(
        _condition_recently_fetched_tweets(),
    ).group_by(
        users.c.id
    ).order_by(
        tw_count.desc()
    ).limit(TOP_USERS_LIMIT)

    return [dict(r) for r in db_engine.execute(query)]


@cache_result(TWEETS_COUNT_RKEY)
def tweets_count() -> int:
    """Returns amount of tweets added in last fetch session."""
    query: Select = select(
        [func.count(tweets.c.id).label('tweets_count')]
    ).where(
        _condition_recently_fetched_tweets(),
    )

    return db_engine.execute(query).first()['tweets_count']


def _condition_recently_fetched_tweets() -> BinaryExpression:
    """Filter tweets which were added in last fetch session."""
    return tweets.c.added_at > _dt_for_last_fetch()


def _dt_for_last_fetch() -> datetime:
    """Returns datetime between last fetch session and now."""
    return datetime.utcnow() - timedelta(minutes=settings.TIME_INTERVAL)

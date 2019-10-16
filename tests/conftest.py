"""Setup test db."""


from datetime import datetime

import pytest
from sqlalchemy import create_engine

from src.settings import DATABASE_URL
from src.tweets.tables import metadata
from src.utils import redis_cli


fixture_queries = {
    'users': '''insert into users (id, screen_name)
    values 
        (1, 'user1'),
        (2, 'user2'),
        (3, 'user3')
    ''',

    'tweets': '''insert into tweets(id, user_id, published_at, text, hashtags, added_at)
    values
        (
            1, 1, '2019-10-09 12:10:01'::timestamp, 'Twit #tag1 #tag2',
            '{{"tag1", "tag2"}}', '{now}'::timestamp
        ),
        (
            2, 1, '2019-10-09 09:23:35'::timestamp, 'Twit #tag1',
            '{{"tag1"}}', '{now}'::timestamp
        ),
        (
            3, 1, '2019-10-09 11:57:52'::timestamp, 'Twit #tag1 #tag2',
            '{{"tag1", "tag2"}}', '{now}'::timestamp
        ),
        (
            4, 2, '2019-10-09 09:23:35'::timestamp, 'Twit #tag1 #tag3 #tag2',
            '{{"tag1", "tag2", "tag3"}}', '{now}'::timestamp
        ),
        (
            5, 2, '2019-10-09 09:23:35'::timestamp, 'Twit #tag1 #tag3',
            '{{"tag1", "tag3"}}', '{now}'::timestamp
        ),
        (
            6, 3, '2019-10-09 09:23:35'::timestamp, 'Twit #tag1',
            '{{"tag1"}}', '{now}'::timestamp
        )
    '''.format(now=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
}


@pytest.yield_fixture(scope='session', autouse=True)
def engine():
    """Create create tables in test db before test session.
    Drops alltables from test db and cleans redis after test session.
    """
    eng = create_engine(DATABASE_URL)
    metadata.create_all(eng)

    for k in fixture_queries:
        eng.execute(fixture_queries[k])

    yield eng

    metadata.drop_all(eng)
    redis_cli.flushall()

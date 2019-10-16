"""Simplified tweets and users db represantation."""

from datetime import datetime

import sqlalchemy as sa


MAX_TWEET_LENGTH = 280

metadata = sa.MetaData()

users = sa.Table(
    'users',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('screen_name', sa.String(50), nullable=False),
)

tweets = sa.Table(
    'tweets',
    metadata,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('user_id', sa.ForeignKey('users.id'), nullable=False),
    sa.Column('published_at', sa.DateTime, nullable=False),
    sa.Column('text', sa.Unicode(MAX_TWEET_LENGTH), nullable=False),
    sa.Column('hashtags', sa.ARRAY(sa.Unicode)),

    # datetime when tweet was added to our system
    sa.Column('added_at', sa.DateTime, nullable=False, default=datetime.utcnow),
)

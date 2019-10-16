"""App settings from .env."""

from starlette.config import Config

config = Config('.env')

DEBUG: bool = config('DEBUG', cast=bool, default=False)
TESTING: bool = config('TESTING', cast=bool, default=False)

POSTGRES_HOST: str = config('POSTGRES_HOST', cast=str)
POSTGRES_PORT: int = config('POSTGRES_PORT', cast=int)
POSTGRES_USER: str = config('POSTGRES_USER', cast=str)
POSTGRES_PASSWORD: str = config('POSTGRES_PASSWORD', cast=str)
POSTGRES_DB: str = config('POSTGRES_DB', cast=str)

if TESTING:
    POSTGRES_DB = f'test_{POSTGRES_DB}'

DATABASE_URL: str = 'postgresql+psycopg2://' \
    f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

TWITTER_CONSUMER_KEY: str = config('TWITTER_CONSUMER_KEY', cast=str)
TWITTER_CONSUMER_SECRET: str = config('TWITTER_CONSUMER_SECRET', cast=str)

TWEETS_COUNT: int = config('TWEETS_COUNT', cast=int, default=500)
TIME_INTERVAL: int = config('TIME_INTERVAL', cast=int, default=10)
PHRASE: str = config('PHRASE', cast=str)

REDIS_HOST: str = config('REDIS_HOST', cast=str, default='redis')
REDIS_PORT: int = config('REDIS_PORT', cast=int, default=6379)

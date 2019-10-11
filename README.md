# tweets
App that fetchet tweets from Twitter and shows their basic statistics.

# Overview
Background task fetches `k` recent tweets by `phrase`. Exposed API allows to see those tweets, their  top hashtags, 
top user who made max amount of tweets, total amount of recently fetched tweets.

## Stack
  - python 3.7
  - postgres 11+
  - redis
  
  Background task performed with [`schedule`](https://pypi.org/project/schedule/) library,
  which is lightweight and simple in comparison to `celery`.
  
  API is created with [`starlette`](https://www.starlette.io/) and hosted with [`uvicorn`](https://www.uvicorn.org/)
  
  All data for API responses is cached in redis.
  
  # Installation
  
   - Clone repository
   > :$ git clone https://github.com/pgtuk/tweets.git
   
   > :$ cd tweets
   
   - Create `.env`
   > :$ cp .env.example .env
   
   - Put your twitter consumer key to `TWITTER_CONSUMER_KEY` and secter to `TWITTER_CONSUMER_SECRET` in `.env`.
   Don't hesitate to change querying phrase `PHRASE`, tweets count `TWEETS_COUNT` and fetching interval `TIME_INTERVAL`.
   Check limits at Twitter API docs
   ## Run in docker 
   > :$ docker-compose up

Note: docker will run linters before starting app, but not tests - requires to add test database.
   
App will be available at '0.0.0.0:5000' by default
   
   ## Run localy
   - If you want to run it locally you'll need python3.7, [`postgres`](https://www.postgresql.org/download/) 
   and [`redis`](https://redis.io/topics/quickstart). Set up databases for deployment and tests. 
   Test DB name assumed to be same as deployment db's name prefixed with `test_`. 
   - Set up python virtual enviroment and install package dependencies
   > $: python3.7 -m venv venv
   
   > $: venv/bin/pip install -r requirements.txt
   
   - Use `make` to run linters, tests and app itself. See `make help` for more information.
   
   
  

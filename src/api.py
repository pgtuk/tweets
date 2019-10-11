"""API methods for tweets."""

from starlette.applications import Starlette

from starlette.schemas import SchemaGenerator
from starlette.responses import JSONResponse

from src import settings
from src.tweets import stats
from src.utils import from_cache


schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Example API", "version": "1.0"}}
)

Api = Starlette(debug=True)


@Api.route('/api/tweets', methods=['GET'])
def list_tweets(_) -> JSONResponse:
    """
    responses:
      200:
        description: A list of users.
        examples:
          [
            {
              "id": 1182368240686784512,
              "user_id":93787352,
              "published_at":"Thu Oct 10 18:52:10 2019",
              "text":"Bom bom bom #bom #secondbom",
              "hashtags":["bom", "secondbom"]
            }
          ]
    """
    return JSONResponse(from_cache(stats.TWEETS_RKEY) or stats.new_tweets())


@Api.route('/api/statistics', methods=['GET'])
def statistics(_):
    """
    responses:
      200:
        description: Tweets statistics - most popular hashtags,
        top users who made max amount of tweets, total tweets count
        examples: {
            "phrase": "bom bom",
            "top_hashtags": [
                {"tag": "bom", "count": 5},
                {"tag": "secondbom", "count": 2},
                {"tag": "thirdbom", "count": 1},
            ],
            "top_users": [
                {"id": 93787352, "screen_name": "bombom_pro","count": 5},
                {"id": 1149722107, "screen_name": "xXxBomBomxXx", "count": 3},
                {"id": 2632353897, "screen_name": "bombom98", "count": 1}
            ],
            "tweets_count": 10
        }
    """
    return JSONResponse({
        'phrase': settings.PHRASE,
        'top_hashtags': from_cache(stats.HASHTAGS_STATS_RKEY) or stats.top_hashtags(),
        'top_users': from_cache(stats.TOP_USERS_RKEY) or stats.top_users(),
        'tweets_count': from_cache(stats.TWEETS_COUNT_RKEY) or stats.tweets_count(),
    })


@Api.route("/api/schema", methods=["GET"], include_in_schema=False)
def openapi_schema(request):
    """Return API schema in .yaml"""
    return schemas.OpenAPIResponse(request=request)

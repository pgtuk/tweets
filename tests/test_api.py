import pytest
from starlette.testclient import TestClient

from src.api import Api
from src import settings


@pytest.fixture(scope='session')
def test_client():
    return TestClient(Api)


def test_list_tweets_endpoint(test_client):
    response = test_client.get(Api.url_path_for('list_tweets'))

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_statistics_enpoind(test_client):
    response = test_client.get(Api.url_path_for('statistics'))

    assert response.status_code == 200
    assert isinstance(response.json(), dict)

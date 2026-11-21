import pytest
from fastapi.testclient import TestClient

from .factories import make_poster
from .upstream import FakeCinemaCity


@pytest.fixture(autouse=True)
def _feeds(upstream: FakeCinemaCity) -> None:
    upstream.stub(
        'feed/10103/allFeedNames',
        [
            {'key': 'now-playing', 'placements': {'home': 0}},
            {'key': 'coming-soon', 'placements': {'home': 1}},
        ],
    )


def test_list_feeds(api: TestClient) -> None:
    response = api.get('/feeds')

    assert response.json() == [
        {'name': 'now-playing', 'placements': {'home': 0}},
        {'name': 'coming-soon', 'placements': {'home': 1}},
    ]


def test_get_feed(api: TestClient) -> None:
    response = api.get('/feeds/coming-soon')

    assert response.json() == {'name': 'coming-soon', 'placements': {'home': 1}}


def test_list_feed_movies(api: TestClient, upstream: FakeCinemaCity) -> None:
    upstream.stub('feed/10103/byName/coming-soon', {'posters': [make_poster('a1')]})

    response = api.get('/feeds/coming-soon/movies')

    assert [movie['id'] for movie in response.json()] == ['a1']


@pytest.mark.parametrize('path', ['/feeds/unknown', '/feeds/unknown/movies'])
def test_feed_endpoints_return_404_for_unknown_feed(api: TestClient, path: str) -> None:
    response = api.get(path)

    assert response.status_code == 404
    assert response.json() == {'detail': "Feed 'unknown' not found."}

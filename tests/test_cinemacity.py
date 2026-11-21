"""Client behaviour not reachable through the REST API."""

from collections.abc import Callable
from datetime import date
from typing import Any
from unittest.mock import patch

import pytest
import requests
from api.cinemacity.client import CinemaCityClient
from api.cinemacity.default import DEFAULT_USER_AGENT
from api.cinemacity.error import CinemaCityAPIError, CinemaCityError
from api.cinemacity.schemas.film import Poster

from .factories import make_poster
from .upstream import BASE_URL, DEFAULT_UNTIL, FakeCinemaCity


@pytest.mark.parametrize(
    ('get_feed', 'feed_name'),
    [
        (CinemaCityClient.get_now_playing, 'now-playing'),
        (CinemaCityClient.get_coming_soon, 'coming-soon'),
    ],
)
def test_featured_feeds(
    cinema_city: CinemaCityClient,
    upstream: FakeCinemaCity,
    get_feed: Callable[[CinemaCityClient], list[Poster]],
    feed_name: str,
) -> None:
    upstream.stub(f'feed/10103/byName/{feed_name}', {'posters': [make_poster('a1')]})

    posters = get_feed(cinema_city)

    assert [poster['code'] for poster in posters] == ['a1']


def test_dates_are_parsed(
    cinema_city: CinemaCityClient, upstream: FakeCinemaCity
) -> None:
    upstream.stub(
        f'quickbook/10103/dates/in-cinema/1064/until/{DEFAULT_UNTIL}',
        {'dates': ['2026-11-20']},
    )

    assert cinema_city.get_dates_in_cinema('1064') == [date(2026, 11, 20)]


def test_owned_session_uses_browser_user_agent_and_is_closed(
    upstream: FakeCinemaCity,
) -> None:
    upstream.stub('feed/10103/allFeedNames', [])

    with (
        patch.object(requests.Session, 'close') as close,
        CinemaCityClient(base_url=BASE_URL) as client,
    ):
        client.get_feed_names()

    assert upstream.last_request.headers['User-Agent'] == DEFAULT_USER_AGENT
    close.assert_called_once()


def test_supplied_session_gets_user_agent_and_is_left_open(
    upstream: FakeCinemaCity,
) -> None:
    upstream.stub('feed/10103/allFeedNames', [])
    session = requests.Session()

    with (
        patch.object(session, 'close') as close,
        CinemaCityClient(
            base_url=BASE_URL, session=session, user_agent='Agent/1.0'
        ) as client,
    ):
        client.get_feed_names()

    assert upstream.last_request.headers['User-Agent'] == 'Agent/1.0'
    close.assert_not_called()


def test_unexpected_empty_response_raises(
    cinema_city: CinemaCityClient, upstream: FakeCinemaCity
) -> None:
    upstream.stub('feed/10103/allFeedNames', status_code=204)

    with pytest.raises(CinemaCityError, match='Unexpected empty response'):
        cinema_city.get_feed_names()


@pytest.mark.parametrize(
    ('response', 'message', 'message_code'),
    [
        (
            {'status_code': 400, 'json': {'message': 'Bad', 'messageCode': 'e.400'}},
            'Bad',
            'e.400',
        ),
        ({'status_code': 400, 'json': {}}, 'Bad Request', None),
        ({'status_code': 400, 'json': ['not', 'an', 'object']}, 'Bad Request', None),
        ({'status_code': 403, 'reason': 'Go away', 'text': '<html/>'}, 'Go away', None),
        ({'status_code': 599, 'text': ''}, 'Unknown error', None),
    ],
    ids=['api-error', 'no-message', 'non-object', 'custom-reason', 'unknown-status'],
)
def test_api_errors_are_parsed(
    cinema_city: CinemaCityClient,
    upstream: FakeCinemaCity,
    response: dict[str, Any],
    message: str,
    message_code: str | None,
) -> None:
    upstream.stub('quickbook/10103/attributes', **response)

    with pytest.raises(CinemaCityAPIError) as raised:
        cinema_city.get_attributes()

    assert raised.value.status_code == response['status_code']
    assert raised.value.message == message
    assert raised.value.message_code == message_code

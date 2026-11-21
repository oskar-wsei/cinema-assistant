from typing import Any

import pytest
import requests
from api.common.config import Settings
from api.main import create_app
from fastapi.testclient import TestClient

from .factories import make_cinema
from .upstream import DEFAULT_UNTIL, FakeCinemaCity

CINEMAS_PATH = f'quickbook/10103/cinemas/with-event/until/{DEFAULT_UNTIL}'


def test_health_does_not_call_upstream(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    response = api.get('/health')

    assert response.json() == {'status': 'ok'}
    assert upstream.request_count == 0


def test_sends_browser_user_agent_upstream(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    upstream.stub(CINEMAS_PATH, {'cinemas': []})

    api.get('/cinemas')

    assert upstream.last_request.headers['User-Agent'].startswith('Mozilla/5.0')


def test_configured_language_is_sent_upstream(
    settings: Settings, upstream: FakeCinemaCity
) -> None:
    upstream.stub(CINEMAS_PATH, {'cinemas': []}, query={'lang': 'en_GB'})
    app = create_app(settings.model_copy(update={'language': 'en_GB'}))

    with TestClient(app) as api:
        assert api.get('/cinemas').status_code == 200


def test_upstream_responses_are_cached(
    settings: Settings, upstream: FakeCinemaCity
) -> None:
    upstream.stub(CINEMAS_PATH, {'cinemas': [make_cinema('1064')]})
    app = create_app(settings.model_copy(update={'cache_ttl_seconds': 60}))

    with TestClient(app) as api:
        first = api.get('/cities')
        second = api.get('/cities/krakow/cinemas')

    assert first.status_code == second.status_code == 200
    assert upstream.request_count == 1


@pytest.mark.parametrize(
    ('response', 'detail'),
    [
        (
            {
                'status_code': 500,
                'json': {
                    'message': 'Server error occurred',
                    'messageCode': 'error.code.500',
                },
            },
            'Cinema City API error: HTTP 500: Server error occurred',
        ),
        (
            {'status_code': 403, 'text': '<html>Blocked</html>'},
            'Cinema City API error: HTTP 403: Forbidden',
        ),
        (
            {'exc': requests.ConnectionError('Connection refused')},
            (
                f"Cinema City API error: Request to '{CINEMAS_PATH}' failed: "
                'Connection refused'
            ),
        ),
        (
            {'json': {'unexpected': 'shape'}},
            f"Cinema City API error: Malformed response for '{CINEMAS_PATH}'",
        ),
    ],
    ids=['api-error', 'bot-protection', 'connection-error', 'malformed-response'],
)
def test_upstream_failures_return_502(
    api: TestClient,
    upstream: FakeCinemaCity,
    response: dict[str, Any],
    detail: str,
) -> None:
    upstream.stub(CINEMAS_PATH, **response)

    result = api.get('/cinemas')

    assert result.status_code == 502
    assert result.json() == {'detail': detail}


def test_openapi_documents_routes_parameters_and_errors(api: TestClient) -> None:
    schema = api.get('/openapi.json').json()

    assert {
        '/movies',
        '/movies/{movie_id}',
        '/movies/{movie_id}/screenings',
        '/cinemas',
        '/cinemas/{cinema_id}',
        '/cinemas/{cinema_id}/trailers',
        '/cities',
        '/cities/{city_id}/cinemas',
    } <= set(schema['paths'])
    operation = schema['paths']['/cinemas/{cinema_id}']['get']
    assert [parameter['name'] for parameter in operation['parameters']] == ['cinema_id']
    assert {'200', '404', '502'} <= set(operation['responses'])

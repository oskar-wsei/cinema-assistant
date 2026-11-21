import pytest
from fastapi.testclient import TestClient

from .factories import make_cinema
from .upstream import DEFAULT_UNTIL, FakeCinemaCity


@pytest.fixture(autouse=True)
def _cinemas(upstream: FakeCinemaCity) -> None:
    upstream.stub(
        f'quickbook/10103/cinemas/with-event/until/{DEFAULT_UNTIL}',
        {
            'cinemas': [
                make_cinema('1064', 'krakow', 'Kraków'),
                make_cinema('1100', 'group-1100', 'Biała Podlaska'),
                make_cinema('1076', 'krakow', 'Kraków'),
            ]
        },
    )


def test_list_cities_derives_cities_from_cinemas_sorted_by_name(
    api: TestClient,
) -> None:
    response = api.get('/cities')

    assert response.json() == [
        {'id': 'group-1100', 'name': 'Biała Podlaska', 'cinema_ids': ['1100']},
        {'id': 'krakow', 'name': 'Kraków', 'cinema_ids': ['1064', '1076']},
    ]


def test_get_city(api: TestClient) -> None:
    response = api.get('/cities/krakow')

    assert response.json() == {
        'id': 'krakow',
        'name': 'Kraków',
        'cinema_ids': ['1064', '1076'],
    }


@pytest.mark.parametrize('path', ['/cities/nowhere', '/cities/nowhere/cinemas'])
def test_city_endpoints_return_404_for_unknown_city(api: TestClient, path: str) -> None:
    response = api.get(path)

    assert response.status_code == 404
    assert response.json() == {'detail': "City 'nowhere' not found."}


def test_list_city_cinemas(api: TestClient) -> None:
    response = api.get('/cities/krakow/cinemas')

    assert [cinema['id'] for cinema in response.json()] == ['1064', '1076']

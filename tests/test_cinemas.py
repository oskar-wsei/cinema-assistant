import pytest
from fastapi.testclient import TestClient

from .factories import make_cinema, make_event, make_film
from .upstream import DEFAULT_UNTIL, TODAY, FakeCinemaCity


@pytest.fixture
def cinema_exists(upstream: FakeCinemaCity) -> None:
    upstream.stub('10103/cinema/1064', {'cinema': make_cinema('1064')})


def test_list_cinemas(api: TestClient, upstream: FakeCinemaCity) -> None:
    upstream.stub(
        f'quickbook/10103/cinemas/with-event/until/{DEFAULT_UNTIL}',
        {'cinemas': [make_cinema('1064')]},
        query={'attr': 'imax,4dx'},
    )

    response = api.get('/cinemas?attribute=imax&attribute=4dx')

    assert response.status_code == 200
    assert response.json() == [
        {
            'id': '1064',
            'name': 'Kraków - 1064',
            'city_id': 'krakow',
            'address': {
                'street': 'ul. Zakopiańska 62',
                'postal_code': '30-418',
                'city': 'Kraków',
            },
            'coordinates': {'latitude': 50.01654, 'longitude': 19.930508},
            'image_url': 'https://example.com/kina/1064.jpg',
            'website_url': 'https://example.com/kina/1064',
        }
    ]


@pytest.mark.usefixtures('cinema_exists')
def test_get_cinema(api: TestClient) -> None:
    response = api.get('/cinemas/1064')

    assert response.status_code == 200
    assert response.json()['name'] == 'Kraków - 1064'


@pytest.mark.parametrize(
    'path', ['', '/trailers', '/screening-dates', '/screenings', '/presales']
)
def test_cinema_endpoints_return_404_for_unknown_cinema(
    api: TestClient, upstream: FakeCinemaCity, path: str
) -> None:
    upstream.stub('10103/cinema/999', status_code=204)

    response = api.get(f'/cinemas/999{path}')

    assert response.status_code == 404
    assert response.json() == {'detail': "Cinema '999' not found."}


@pytest.mark.usefixtures('cinema_exists')
def test_list_cinema_trailers(api: TestClient, upstream: FakeCinemaCity) -> None:
    upstream.stub(
        '10103/trailers/byCinemaId/1064',
        [
            {
                'filmId': 'a1',
                'filmName': 'Alpha',
                'filmLink': 'https://example.com/filmy/a1',
                'videoLink': None,
            }
        ],
    )

    response = api.get('/cinemas/1064/trailers')

    assert response.json() == [
        {
            'movie_id': 'a1',
            'movie_title': 'Alpha',
            'movie_url': 'https://example.com/filmy/a1',
            'video_url': None,
        }
    ]


@pytest.mark.usefixtures('cinema_exists')
def test_list_cinema_screening_dates(api: TestClient, upstream: FakeCinemaCity) -> None:
    upstream.stub(
        'quickbook/10103/dates/in-cinema/1064/until/2026-12-31',
        {'dates': ['2026-11-20', '2026-11-21']},
        query={'attr': 'imax'},
    )

    response = api.get('/cinemas/1064/screening-dates?until=2026-12-31&attribute=imax')

    assert response.json() == ['2026-11-20', '2026-11-21']


@pytest.mark.usefixtures('cinema_exists')
def test_list_cinema_screenings_groups_by_movie_sorted_by_start(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    upstream.stub(
        'quickbook/10103/film-events/in-cinema/1064/at-date/2026-11-20',
        {
            'films': [make_film('a1'), make_film('b2')],
            'events': [
                make_event('b2-1', film_id='b2'),
                make_event('a1-2', film_id='a1', starts_at='2026-11-20T20:00:00'),
                make_event('a1-1', film_id='a1', starts_at='2026-11-20T12:00:00'),
            ],
        },
    )

    response = api.get('/cinemas/1064/screenings?date=2026-11-20')

    by_movie = {
        group['movie']['id']: [screening['id'] for screening in group['screenings']]
        for group in response.json()
    }
    assert by_movie == {'a1': ['a1-1', 'a1-2'], 'b2': ['b2-1']}
    screening = response.json()[0]['screenings'][0]
    assert screening['starts_at'] == '2026-11-20T12:00:00'
    assert screening['business_date'] == '2026-11-20'
    assert screening['seat_availability'] == 0.75
    assert screening['booking_url'] == 'https://example.com/order/a1-1'


@pytest.mark.usefixtures('cinema_exists')
def test_list_cinema_screenings_defaults_to_today(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    upstream.stub(
        f'quickbook/10103/film-events/in-cinema/1064/at-date/{TODAY}',
        {'films': [], 'events': []},
        query={'attr': 'dubbed'},
    )

    response = api.get('/cinemas/1064/screenings?attribute=dubbed')

    assert response.json() == []


@pytest.mark.usefixtures('cinema_exists')
def test_list_cinema_presales(api: TestClient, upstream: FakeCinemaCity) -> None:
    upstream.stub(
        'quickbook/10103/film-events-dates/in-cinema/1064/as-at-date/2026-11-20',
        {
            'films': [make_film('a1')],
            'eventsDatesByFilmId': {'a1': ['2026-12-01', '2026-12-02']},
        },
    )

    response = api.get('/cinemas/1064/presales?as_of=2026-11-20')

    [presale] = response.json()
    assert presale['movie']['id'] == 'a1'
    assert presale['movie']['duration_minutes'] == 158
    assert presale['screening_dates'] == ['2026-12-01', '2026-12-02']


@pytest.mark.usefixtures('cinema_exists')
def test_list_cinema_presales_defaults_to_today(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    upstream.stub(
        f'quickbook/10103/film-events-dates/in-cinema/1064/as-at-date/{TODAY}',
        {'films': [], 'eventsDatesByFilmId': {}},
    )

    assert api.get('/cinemas/1064/presales').json() == []

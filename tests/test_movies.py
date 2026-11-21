import pytest
from fastapi.testclient import TestClient

from .factories import (
    make_cinema,
    make_cinema_with_events,
    make_event,
    make_film,
    make_film_details,
    make_poster,
)
from .upstream import DEFAULT_UNTIL, TODAY, FakeCinemaCity


@pytest.fixture
def movie_exists(upstream: FakeCinemaCity) -> None:
    upstream.stub(
        '10103/films/byDistributorCode/7803s2r',
        {'filmDetails': make_film_details('7803s2r')},
    )


@pytest.mark.parametrize(
    ('query', 'showing_type'),
    [
        ('', 'ALL'),
        ('?status=showing', 'SHOWING'),
        ('?status=upcoming', 'FUTURE'),
        ('?status=past', 'PAST'),
    ],
)
def test_list_movies_by_status(
    api: TestClient, upstream: FakeCinemaCity, query: str, showing_type: str
) -> None:
    upstream.stub(
        f'poster/10103/by-showing-type/{showing_type}',
        {'posters': [make_poster('a1', 'Alpha')]},
    )

    response = api.get(f'/movies{query}')

    assert response.status_code == 200
    [movie] = response.json()
    assert movie == {
        'id': 'a1',
        'title': 'Alpha',
        'poster_url': 'https://example.com/posters/a1.jpg',
        'trailer_url': 'https://youtube.com/watch?v=trailer',
        'website_url': 'https://example.com/filmy/a1',
        'release_date': '2026-11-20',
        'duration_minutes': None,
        'attributes': ['2d', 'action'],
        'languages': {
            'original': ['en'],
            'dubbed': ['pl'],
            'voiceover': [],
            'subtitles': ['pl'],
        },
    }


def test_list_movies_filters_by_cinema_and_attributes(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    upstream.stub(
        'poster/10103/by-showing-type/SHOWING',
        {'posters': []},
        query={'cinemaId': '1064', 'attr': '4dx,imax'},
    )

    response = api.get(
        '/movies?status=showing&cinema_id=1064&attribute=4dx&attribute=imax'
    )

    assert response.json() == []


def test_list_movies_rejects_unknown_status(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    assert api.get('/movies?status=bogus').status_code == 422
    assert upstream.request_count == 0


def test_list_bookable_movies(api: TestClient, upstream: FakeCinemaCity) -> None:
    upstream.stub(
        f'quickbook/10103/films/until/{DEFAULT_UNTIL}',
        {'films': [make_film('a1', 'Alpha')]},
    )

    [movie] = api.get('/movies/bookable').json()

    assert movie['id'] == 'a1'
    assert movie['duration_minutes'] == 158
    assert movie['trailer_url'] is None


@pytest.mark.usefixtures('movie_exists')
def test_get_movie(api: TestClient) -> None:
    response = api.get('/movies/7803s2r')

    assert response.status_code == 200
    movie = response.json()
    assert movie['title'] == 'Igrzyska śmierci'
    assert movie['original_title'] == 'The Hunger Games'
    assert movie['status'] == 'upcoming'
    assert movie['poster_url'] == 'https://example.com/posters/7803s2r-lg.jpg'
    assert movie['cast'] == ['Joseph Zada', 'Elle Fanning', 'Jesse Plemons']
    assert movie['directors'] == ['Francis Lawrence']
    assert movie['release_year'] == 2026
    assert movie['genres'] == ['action']
    assert movie['attributes'] == ['2d', 'imax', 'action']
    assert movie['age_rating'] == {
        'code': '15-plus',
        'icon_url': 'https://example.com/rating/15.png',
    }
    assert movie['screening_count'] == 42


def test_get_movie_with_missing_optional_details(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    details = make_film_details('a1')
    details.update(
        {'cast': None, 'directors': None, 'releaseYear': None, 'length': None}
    )
    upstream.stub('10103/films/byDistributorCode/a1', {'filmDetails': details})

    movie = api.get('/movies/a1').json()

    assert movie['cast'] == []
    assert movie['directors'] == []
    assert movie['release_year'] is None
    assert movie['duration_minutes'] is None


@pytest.mark.parametrize(
    'path',
    ['', '/cities', '/screening-dates?city_id=krakow', '/screenings?city_id=krakow'],
)
def test_movie_endpoints_return_404_for_unknown_movie(
    api: TestClient, upstream: FakeCinemaCity, path: str
) -> None:
    upstream.stub('10103/films/byDistributorCode/unknown', status_code=204)

    response = api.get(f'/movies/unknown{path}')

    assert response.status_code == 404
    assert response.json() == {'detail': "Movie 'unknown' not found."}


@pytest.mark.usefixtures('movie_exists')
def test_list_movie_cities_uses_canonical_city_names(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    upstream.stub(
        f'quickbook/10103/cinemas/with-event/until/{DEFAULT_UNTIL}',
        {'cinemas': [make_cinema('1088', 'bielsko-biala', 'Bielsko-Biała')]},
    )
    upstream.stub(
        'quickbook/10103/groups/with-film/7803s2r/until/2026-12-31',
        {
            'groups': [
                {'id': 'bielsko-biala', 'name': 'Bielsko Biała', 'cinemaIds': ['1088']},
                {'id': 'new-city', 'name': 'New City', 'cinemaIds': ['2000']},
            ]
        },
        query={'attr': 'imax'},
    )

    response = api.get('/movies/7803s2r/cities?until=2026-12-31&attribute=imax')

    assert response.json() == [
        {'id': 'bielsko-biala', 'name': 'Bielsko-Biała', 'cinema_ids': ['1088']},
        {'id': 'new-city', 'name': 'New City', 'cinema_ids': ['2000']},
    ]


@pytest.mark.usefixtures('movie_exists')
def test_list_movie_screening_dates_in_city(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    upstream.stub(
        f'quickbook/10103/dates/in-group/krakow/with-film/7803s2r/until/{DEFAULT_UNTIL}',
        {'dates': ['2026-11-20']},
        query={'attr': 'imax'},
    )

    response = api.get('/movies/7803s2r/screening-dates?city_id=krakow&attribute=imax')

    assert response.json() == ['2026-11-20']


@pytest.mark.usefixtures('movie_exists')
def test_list_movie_screening_dates_in_cinemas(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    upstream.stub(
        'quickbook/10103/dates/with-film/7803s2r/until/2026-12-31',
        {'dates': ['2026-11-21']},
        query={'ids': '1064,1076'},
    )

    response = api.get(
        '/movies/7803s2r/screening-dates?cinema_id=1064&cinema_id=1076&until=2026-12-31'
    )

    assert response.json() == ['2026-11-21']


@pytest.mark.usefixtures('movie_exists')
def test_list_movie_screenings_in_city_groups_by_cinema_sorted_by_start(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    upstream.stub(
        'quickbook/10103/cinema-events/in-group/krakow/with-film/7803s2r'
        '/at-date/2026-11-20',
        {
            'cinemas': [
                make_cinema_with_events('1064'),
                make_cinema_with_events('1076'),
            ],
            'events': [
                make_event('late', cinema_id='1064', starts_at='2026-11-20T21:00:00'),
                make_event('other', cinema_id='1076', starts_at='2026-11-20T19:00:00'),
                make_event('early', cinema_id='1064', starts_at='2026-11-20T10:00:00'),
            ],
        },
    )

    response = api.get('/movies/7803s2r/screenings?city_id=krakow&date=2026-11-20')

    by_cinema = {
        group['cinema']['id']: [screening['id'] for screening in group['screenings']]
        for group in response.json()
    }
    assert by_cinema == {'1064': ['early', 'late'], '1076': ['other']}


@pytest.mark.usefixtures('movie_exists')
def test_list_movie_screenings_in_cinemas_defaults_to_today(
    api: TestClient, upstream: FakeCinemaCity
) -> None:
    upstream.stub(
        f'quickbook/10103/cinema-events/with-film/7803s2r/at-date/{TODAY}',
        {'cinemas': [], 'events': []},
        query={'ids': '1064,1076', 'attr': 'dubbed'},
    )

    response = api.get(
        '/movies/7803s2r/screenings?cinema_id=1064&cinema_id=1076&attribute=dubbed'
    )

    assert response.json() == []


@pytest.mark.parametrize('resource', ['screenings', 'screening-dates'])
@pytest.mark.parametrize('location', ['', '?city_id=krakow&cinema_id=1064'])
def test_movie_screening_endpoints_require_exactly_one_location(
    api: TestClient, upstream: FakeCinemaCity, resource: str, location: str
) -> None:
    response = api.get(f'/movies/7803s2r/{resource}{location}')

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == (
        'Provide exactly one of `city_id` or `cinema_id`.'
    )
    assert upstream.request_count == 0

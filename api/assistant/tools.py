import unicodedata
from functools import cache
from typing import Any
from urllib.parse import quote

import requests

from .tool import Tool, type_object, type_string

API_URL = 'http://localhost:8000'

_DATE_PARAM = type_string('Date in format YYYY-MM-DD.')


class ToolError(Exception):
    pass


def _get(path: str, params: dict[str, Any] | None = None) -> Any:
    params = {key: value for key, value in (params or {}).items() if value}
    res = requests.get(f'{API_URL}{path}', params=params)
    if not res.ok:
        try:
            detail = res.json().get('detail')
        except ValueError:
            detail = res.text
        raise ToolError(f'API error {res.status_code}: {detail}')
    return res.json()


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize('NFKD', text.casefold().replace('ł', 'l'))
    return ''.join(c for c in decomposed if not unicodedata.combining(c))


def _screening(screening: dict[str, Any]) -> dict[str, Any]:
    attributes = _screening_attributes()
    return {
        'time': screening['starts_at'],
        'format': ' '.join(a for a in screening['attributes'] if a in attributes),
        'sold_out': screening['sold_out'],
    }


@cache
def _screening_attributes() -> frozenset[str]:
    """Attributes that tell screenings apart, e.g. `imax` or `dubbed`; no genres."""
    groups = {group['name']: group['attributes'] for group in _get('/attributes')}
    ids = [
        attribute['id']
        for name in ('screening-type', 'special-type', 'extra', 'language')
        for attribute in groups.get(name, [])
    ]
    return frozenset(id_ for id_ in ids if '-lang-' not in id_)


class ListCinemasTool(Tool):
    def __init__(self):
        super().__init__(
            name='list_cinemas',
            description='Retrieve the list of cinemas with their ids, cities and addresses.',
        )

    def execute(self, args: dict[str, Any]) -> Any:
        return [
            {
                'id': cinema['id'],
                'name': cinema['name'],
                'city_id': cinema['city_id'],
                'street': cinema['address']['street'],
                'postal_code': cinema['address']['postal_code'],
                'city': cinema['address']['city'],
            }
            for cinema in _get('/cinemas')
        ]


class ListMoviesTool(Tool):
    def __init__(self):
        super().__init__(
            name='list_movies',
            description=(
                'List movies that are showing now or coming soon, with their ids. '
                'Use the title filter to find the movie_id of a specific movie.'
            ),
            parameters=type_object(
                optional={
                    'title': type_string(
                        'Only movies whose title contains this text. Titles are in Polish.'
                    ),
                    'status': type_string(
                        'Whether to list movies showing now or coming soon.',
                        enum=['showing', 'upcoming'],
                    ),
                    'cinema_id': type_string(
                        'Numeric cinema id. Only show movies screened in this cinema, see list_cinemas.'
                    ),
                },
            ),
        )

    def execute(self, args: dict[str, Any]) -> Any:
        status = args.get('status') or 'showing'
        title = _normalize(args.get('title') or '')
        movies = _get('/movies', {'status': status, 'cinema_id': args.get('cinema_id')})
        return [
            {
                'id': movie['id'],
                'title': movie['title'],
                'release_date': movie['release_date'],
            }
            for movie in movies
            if title in _normalize(movie['title'])
        ]


class GetMovieDetailsTool(Tool):
    def __init__(self):
        super().__init__(
            name='get_movie_details',
            description=(
                'Get details of one movie the user asks about: synopsis, duration, '
                'genres, cast, directors, age rating and language versions. '
                'Do not call it for every movie in a list.'
            ),
            parameters=type_object(
                required={
                    'movie_id': type_string('Movie hexadecimal id, see list_movies.')
                },
            ),
        )

    def execute(self, args: dict[str, Any]) -> Any:
        movie = _get(f'/movies/{quote(args["movie_id"], safe="")}')
        return {
            'id': movie['id'],
            'title': movie['title'],
            'original_title': movie['original_title'],
            'status': movie['status'],
            'release_date': movie['release_date'],
            'duration_minutes': movie['duration_minutes'],
            'genres': movie['genres'],
            'age_rating': movie['age_rating']['code'],
            'synopsis': movie['synopsis'],
            'cast': movie['cast'],
            'directors': movie['directors'],
            'production': [movie['release_country'], movie['release_year']],
            'languages': movie['languages'],
        }


class ListMovieScreeningsTool(Tool):
    def __init__(self):
        super().__init__(
            name='list_movie_screenings',
            description=(
                'List screenings of a movie on a given day in all cinemas of a city '
                'or in one cinema, with start times and formats such as IMAX, '
                'dubbed or subbed. Provide exactly one of city_id or cinema_id.'
            ),
            parameters=type_object(
                required={
                    'movie_id': type_string('Movie hexadecimal id, see list_movies.')
                },
                optional={
                    'city_id': type_string('City id, see city_id in list_cinemas.'),
                    'cinema_id': type_string('Cinema numeric id, see list_cinemas.'),
                    'date': _DATE_PARAM,
                },
            ),
        )

    def execute(self, args: dict[str, Any]) -> Any:
        cinemas = _get(
            f'/movies/{quote(args["movie_id"], safe="")}/screenings',
            {
                'city_id': args.get('city_id'),
                'cinema_id': args.get('cinema_id'),
                'date': args.get('date'),
            },
        )
        return [
            {
                'cinema': cinema['cinema']['name'],
                'cinema_id': cinema['cinema']['id'],
                'screenings': [_screening(s) for s in cinema['screenings']],
            }
            for cinema in cinemas
        ]


class ListCinemaScreeningsTool(Tool):
    def __init__(self):
        super().__init__(
            name='list_cinema_screenings',
            description=(
                'List the repertoire of a cinema on a given day: '
                'all movies with their screening times and formats.'
            ),
            parameters=type_object(
                required={'cinema_id': type_string('Cinema numeric id, see list_cinemas.')},
                optional={'date': _DATE_PARAM},
            ),
        )

    def execute(self, args: dict[str, Any]) -> Any:
        movies = _get(
            f'/cinemas/{quote(args["cinema_id"], safe="")}/screenings',
            {'date': args.get('date')},
        )
        return [
            {
                'movie': movie['movie']['title'],
                'movie_id': movie['movie']['id'],
                'duration_minutes': movie['movie']['duration_minutes'],
                'screenings': [_screening(s) for s in movie['screenings']],
            }
            for movie in movies
        ]


TOOLS = [
    ListCinemasTool(),
    ListMoviesTool(),
    GetMovieDetailsTool(),
    ListMovieScreeningsTool(),
    ListCinemaScreeningsTool(),
]

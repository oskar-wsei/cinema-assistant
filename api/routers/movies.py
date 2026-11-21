from datetime import date
from typing import Annotated, assert_never

from fastapi import APIRouter, Query

from .. import cinemacity as cc
from ..common.dependencies import (
    CinemasLocation,
    CitiesDep,
    CityLocation,
    ClientDep,
    ExistingMovie,
    LocationDep,
)
from ..common.errors import NOT_FOUND_RESPONSE, UPSTREAM_ERROR_RESPONSE
from ..common.parameters import AttributesQuery, DateQuery, UntilQuery
from ..schemas.cinemas import City
from ..schemas.movies import Movie, MovieDetails, MovieStatus
from ..schemas.screenings import CinemaScreenings

router = APIRouter(prefix='/movies', tags=['Movies'], responses=UPSTREAM_ERROR_RESPONSE)


@router.get('', summary='List movies')
def list_movies(
    client: ClientDep,
    status: Annotated[
        MovieStatus | None,
        Query(description='Only movies with this status. Omit to list all movies.'),
    ] = None,
    cinema_id: Annotated[
        str | None,
        Query(description='Only movies screened in this cinema.', examples=['1064']),
    ] = None,
    attributes: AttributesQuery = None,
) -> list[Movie]:
    showing_type: cc.PosterShowingType = status.to_cinema_city() if status else 'ALL'
    posters = client.get_posters(
        showing_type, cinema_id=cinema_id, attributes=attributes
    )
    return [Movie.from_poster(poster) for poster in posters]


@router.get('/bookable', summary='List bookable movies')
def list_bookable_movies(
    client: ClientDep, until: UntilQuery = None, attributes: AttributesQuery = None
) -> list[Movie]:
    films = client.get_films(until=until, attributes=attributes)
    return [Movie.from_film(film) for film in films]


@router.get('/{movie_id}', summary='Get a movie', responses=NOT_FOUND_RESPONSE)
def get_movie(movie: ExistingMovie) -> MovieDetails:
    return MovieDetails.from_cinema_city(movie)


@router.get(
    '/{movie_id}/cities',
    summary='List cities screening a movie',
    responses=NOT_FOUND_RESPONSE,
)
def list_movie_cities(
    movie: ExistingMovie,
    client: ClientDep,
    cities: CitiesDep,
    until: UntilQuery = None,
    attributes: AttributesQuery = None,
) -> list[City]:
    city_names = {city.id: city.name for city in cities}
    groups = client.get_cinema_groups_with_film(
        movie['id'], until=until, attributes=attributes
    )
    return [
        City(
            id=group['id'],
            name=city_names.get(group['id'], group['name']),
            cinema_ids=group['cinemaIds'],
        )
        for group in groups
    ]


@router.get(
    '/{movie_id}/screening-dates',
    summary='List days with screenings of a movie',
    responses=NOT_FOUND_RESPONSE,
)
def list_movie_screening_dates(
    location: LocationDep,
    movie: ExistingMovie,
    client: ClientDep,
    until: UntilQuery = None,
    attributes: AttributesQuery = None,
) -> list[date]:
    match location:
        case CityLocation(city_id):
            return client.get_dates_for_film_in_group(
                city_id, movie['id'], until=until, attributes=attributes
            )
        case CinemasLocation(cinema_ids):
            return client.get_dates_for_film_in_cinemas(
                movie['id'], cinema_ids, until=until, attributes=attributes
            )
        case _:
            assert_never(location)


@router.get(
    '/{movie_id}/screenings',
    summary='List screenings of a movie',
    responses=NOT_FOUND_RESPONSE,
)
def list_movie_screenings(
    location: LocationDep,
    movie: ExistingMovie,
    client: ClientDep,
    on_date: DateQuery = None,
    attributes: AttributesQuery = None,
) -> list[CinemaScreenings]:
    day = on_date or date.today()
    match location:
        case CityLocation(city_id):
            events = client.get_cinema_events_for_film_in_group(
                city_id, movie['id'], day, attributes=attributes
            )
        case CinemasLocation(cinema_ids):
            events = client.get_cinema_events_for_film_in_cinemas(
                movie['id'], cinema_ids, day, attributes=attributes
            )
        case _:
            assert_never(location)
    return CinemaScreenings.group(events)

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request, status
from fastapi.exceptions import RequestValidationError

from .. import cinemacity as cc
from ..common.parameters import CinemaIdPath, CityIdPath, MovieIdPath
from ..schemas.cinemas import City


def get_client(request: Request) -> cc.client.CinemaCityClient:
    client: cc.client.CinemaCityClient = request.app.state.client
    return client


ClientDep = Annotated[cc.client.CinemaCityClient, Depends(get_client)]


def get_cinema_or_404(
    cinema_id: CinemaIdPath, client: ClientDep
) -> cc.schemas.cinema.Cinema:
    cinema = client.get_cinema(cinema_id)
    if cinema is None:
        raise _not_found(f'Cinema {cinema_id!r} not found.')
    return cinema


def get_movie_or_404(
    movie_id: MovieIdPath, client: ClientDep
) -> cc.schemas.film.FilmDetails:
    movie = client.get_film_details(movie_id)
    if movie is None:
        raise _not_found(f'Movie {movie_id!r} not found.')
    return movie


def get_cities(client: ClientDep) -> list[City]:
    return City.from_cinemas(client.get_cinemas())


CitiesDep = Annotated[list[City], Depends(get_cities)]


def get_city_or_404(city_id: CityIdPath, cities: CitiesDep) -> City:
    city = next((city for city in cities if city.id == city_id), None)
    if city is None:
        raise _not_found(f'City {city_id!r} not found.')
    return city


ExistingCinema = Annotated[cc.schemas.cinema.Cinema, Depends(get_cinema_or_404)]
ExistingMovie = Annotated[cc.schemas.film.FilmDetails, Depends(get_movie_or_404)]
ExistingCity = Annotated[City, Depends(get_city_or_404)]


@dataclass(frozen=True)
class CityLocation:
    city_id: str


@dataclass(frozen=True)
class CinemasLocation:
    cinema_ids: list[str]


type Location = CityLocation | CinemasLocation


def get_location(
    city_id: Annotated[
        str | None,
        Query(description='Search in all cinemas of this city.', examples=['krakow']),
    ] = None,
    cinema_ids: Annotated[
        list[str] | None,
        Query(
            alias='cinema_id',
            description='Search in this cinema. Repeatable.',
            examples=[['1064', '1076']],
        ),
    ] = None,
) -> Location:
    """Exactly one of ``city_id`` and ``cinema_id`` must be provided."""
    if city_id is not None and not cinema_ids:
        return CityLocation(city_id)
    if cinema_ids and city_id is None:
        return CinemasLocation(cinema_ids)
    raise RequestValidationError(
        [
            {
                'type': 'value_error',
                'loc': ('query', 'city_id|cinema_id'),
                'msg': 'Provide exactly one of `city_id` or `cinema_id`.',
                'input': {'city_id': city_id, 'cinema_id': cinema_ids},
            }
        ]
    )


LocationDep = Annotated[Location, Depends(get_location)]


def _not_found(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

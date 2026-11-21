from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query

from ..common.dependencies import ClientDep, ExistingCinema
from ..common.errors import NOT_FOUND_RESPONSE, UPSTREAM_ERROR_RESPONSE
from ..common.parameters import AttributesQuery, DateQuery, UntilQuery
from ..schemas.cinemas import Cinema
from ..schemas.movies import Trailer
from ..schemas.screenings import MovieScreenings, PresaleMovie

router = APIRouter(
    prefix='/cinemas', tags=['Cinemas'], responses=UPSTREAM_ERROR_RESPONSE
)


@router.get('', summary='List cinemas')
def list_cinemas(client: ClientDep, attributes: AttributesQuery = None) -> list[Cinema]:
    return [
        Cinema.from_cinema_city(cinema)
        for cinema in client.get_cinemas(attributes=attributes)
    ]


@router.get('/{cinema_id}', summary='Get a cinema', responses=NOT_FOUND_RESPONSE)
def get_cinema(cinema: ExistingCinema) -> Cinema:
    return Cinema.from_cinema_city(cinema)


@router.get(
    '/{cinema_id}/trailers',
    summary='List trailers of movies screened in a cinema',
    responses=NOT_FOUND_RESPONSE,
)
def list_cinema_trailers(cinema: ExistingCinema, client: ClientDep) -> list[Trailer]:
    trailers = client.get_trailers_in_cinema(cinema['id'])
    return [Trailer.from_cinema_city(trailer) for trailer in trailers]


@router.get(
    '/{cinema_id}/screening-dates',
    summary='List days with screenings in a cinema',
    responses=NOT_FOUND_RESPONSE,
)
def list_cinema_screening_dates(
    cinema: ExistingCinema,
    client: ClientDep,
    until: UntilQuery = None,
    attributes: AttributesQuery = None,
) -> list[date]:
    return client.get_dates_in_cinema(cinema['id'], until=until, attributes=attributes)


@router.get(
    '/{cinema_id}/screenings',
    summary='List screenings in a cinema',
    responses=NOT_FOUND_RESPONSE,
)
def list_cinema_screenings(
    cinema: ExistingCinema,
    client: ClientDep,
    on_date: DateQuery = None,
    attributes: AttributesQuery = None,
) -> list[MovieScreenings]:
    film_events = client.get_film_events_in_cinema(
        cinema['id'], on_date or date.today(), attributes=attributes
    )
    return MovieScreenings.group(film_events)


@router.get(
    '/{cinema_id}/presales',
    summary='List presale movies in a cinema',
    responses=NOT_FOUND_RESPONSE,
)
def list_cinema_presales(
    cinema: ExistingCinema,
    client: ClientDep,
    as_of: Annotated[
        date | None,
        Query(description='Reference day for "not yet released". Defaults to today.'),
    ] = None,
    attributes: AttributesQuery = None,
) -> list[PresaleMovie]:
    presales = client.get_presale_films_in_cinema(
        cinema['id'], as_of or date.today(), attributes=attributes
    )
    return PresaleMovie.from_cinema_city(presales)

from fastapi import APIRouter

from ..common.dependencies import CitiesDep, ClientDep, ExistingCity
from ..common.errors import NOT_FOUND_RESPONSE, UPSTREAM_ERROR_RESPONSE
from ..schemas.cinemas import Cinema, City

router = APIRouter(prefix='/cities', tags=['Cities'], responses=UPSTREAM_ERROR_RESPONSE)


@router.get('', summary='List cities')
def list_cities(cities: CitiesDep) -> list[City]:
    return cities


@router.get('/{city_id}', summary='Get a city', responses=NOT_FOUND_RESPONSE)
def get_city(city: ExistingCity) -> City:
    return city


@router.get(
    '/{city_id}/cinemas',
    summary='List cinemas in a city',
    responses=NOT_FOUND_RESPONSE,
)
def list_city_cinemas(city: ExistingCity, client: ClientDep) -> list[Cinema]:
    return [
        Cinema.from_cinema_city(cinema)
        for cinema in client.get_cinemas()
        if cinema['groupId'] == city.id
    ]

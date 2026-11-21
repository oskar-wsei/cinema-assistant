from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import Self

from pydantic import Field

from .. import cinemacity as cc
from ..schemas.common import ApiModel


class Address(ApiModel):
    street: str = Field(examples=['ul. Zakopiańska 62'])
    postal_code: str = Field(examples=['30-418'])
    city: str = Field(examples=['Kraków'])


class Coordinates(ApiModel):
    latitude: float = Field(examples=[50.01654])
    longitude: float = Field(examples=[19.930508])


class Cinema(ApiModel):
    id: str = Field(examples=['1064'])
    name: str = Field(examples=['Kraków - Zakopianka'])
    city_id: str = Field(examples=['krakow'])
    address: Address
    coordinates: Coordinates
    image_url: str
    website_url: str = Field(description='Cinema page on the Cinema City website.')

    @classmethod
    def from_cinema_city(cls, cinema: cc.schemas.cinema.Cinema) -> Self:
        address = cinema['addressInfo']
        return cls(
            id=cinema['id'],
            name=cinema['displayName'],
            city_id=cinema['groupId'],
            address=Address(
                street=address['address1'],
                postal_code=address['postalCode'],
                city=address['city'],
            ),
            coordinates=Coordinates(
                latitude=cinema['latitude'], longitude=cinema['longitude']
            ),
            image_url=cinema['imageUrl'],
            website_url=cinema['link'],
        )


class City(ApiModel):
    id: str = Field(examples=['krakow'])
    name: str = Field(examples=['Kraków'])
    cinema_ids: list[str] = Field(examples=[['1064', '1076', '1090']])

    @classmethod
    def from_cinemas(cls, cinemas: Iterable[cc.schemas.cinema.Cinema]) -> list[Self]:
        cinemas_by_city: defaultdict[str, list[cc.schemas.cinema.Cinema]] = defaultdict(
            list
        )
        for cinema in cinemas:
            cinemas_by_city[cinema['groupId']].append(cinema)
        cities = [
            cls(
                id=city_id,
                name=_most_common_town(city_cinemas),
                cinema_ids=[cinema['id'] for cinema in city_cinemas],
            )
            for city_id, city_cinemas in cinemas_by_city.items()
        ]
        return sorted(cities, key=lambda city: city.name)


def _most_common_town(cinemas: list[cc.schemas.cinema.Cinema]) -> str:
    towns = Counter(cinema['addressInfo']['city'] for cinema in cinemas)
    return towns.most_common(1)[0][0]

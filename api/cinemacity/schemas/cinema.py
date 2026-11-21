from typing import TypedDict

from .common import AddressInfo
from .film import Languages


class Cinema(TypedDict):
    id: str
    groupId: str
    displayName: str
    link: str
    imageUrl: str
    address: str
    addressInfo: AddressInfo
    latitude: float
    longitude: float
    bookingUrl: str | None
    blockOnlineSales: bool
    blockOnlineSalesUntil: str | None


class CinemaWithEvents(Cinema):
    attributeIds: list[str]
    languages: Languages


class CinemaGroup(TypedDict):
    id: str
    name: str
    cinemaIds: list[str]

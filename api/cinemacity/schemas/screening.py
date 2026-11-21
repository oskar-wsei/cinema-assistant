from typing import TypedDict

from .cinema import CinemaWithEvents
from .common import Languages
from .film import Film


class BookingUrlParams(TypedDict):
    lang: str


class BookingUrl(TypedDict):
    url: str
    params: BookingUrlParams


class CompositeBookingLink(TypedDict):
    type: str
    bookingUrl: BookingUrl
    obsoleteBookingUrl: str
    serviceUrl: str
    blockOnlineSales: bool
    blockOnlineSalesUntil: str | None


class Event(TypedDict):
    id: str
    filmId: str
    cinemaId: str
    businessDay: str
    eventDateTime: str
    auditorium: str
    auditoriumTinyName: str
    availabilityRatio: float
    soldOut: bool
    presentationCode: str
    attributeIds: list[str]
    languages: Languages
    bookingLink: str
    bookingRouterLaunchLink: str
    compositeBookingLink: CompositeBookingLink


class FilmEvents(TypedDict):
    films: list[Film]
    events: list[Event]


class CinemaEvents(TypedDict):
    cinemas: list[CinemaWithEvents]
    events: list[Event]


class PresaleFilms(TypedDict):
    films: list[Film]
    eventsDatesByFilmId: dict[str, list[str]]

from collections.abc import Mapping
from typing import TypedDict

from .schemas.cinema import Cinema, CinemaGroup
from .schemas.film import Film, FilmDetails, Poster

type QueryParams = Mapping[str, str]


class PostersBody(TypedDict):
    posters: list[Poster]


class FilmsBody(TypedDict):
    films: list[Film]


class FilmDetailsBody(TypedDict):
    filmDetails: FilmDetails


class CinemasBody(TypedDict):
    cinemas: list[Cinema]


class CinemaBody(TypedDict):
    cinema: Cinema


class GroupsBody(TypedDict):
    groups: list[CinemaGroup]


class DatesBody(TypedDict):
    dates: list[str]

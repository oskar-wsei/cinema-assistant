from typing import Literal, TypedDict

from .common import Languages, Media

FilmShowingType = Literal['SHOWING', 'FUTURE', 'PAST']

PosterShowingType = Literal['SHOWING', 'FUTURE', 'PAST', 'ALL']


class Poster(TypedDict):
    code: str
    featureTitle: str
    url: str
    posterSrc: str
    weight: int
    dateStarted: str
    filmShowingType: FilmShowingType
    attributes: list[str]
    languages: Languages
    mediaList: list[Media]


class FeedName(TypedDict):
    key: str
    placements: dict[str, int]


class Film(TypedDict):
    id: str
    name: str
    length: int | None
    posterLink: str
    videoLink: str | None
    link: str
    weight: int
    releaseYear: str | None
    releaseDate: str
    attributeIds: list[str]
    languages: Languages


class FilmDetails(TypedDict):
    id: str
    name: str
    originalName: str
    length: int | None
    synopsis: str
    cast: str | None
    directors: str | None
    releaseYear: str | None
    releaseCountry: str | None
    dateStarted: str
    showingType: FilmShowingType
    weight: int
    eventCount: int
    link: str
    posterLink: str
    posterLinkLarge: str
    videoLink: str | None
    mediaList: list[Media]
    distributorName: str | None
    specialMessage: str | None
    ageRestrictionId: int
    ageRestrictionName: str
    ageRestrictionLink: str
    ageRestrictionDescription: str | None
    categoryIds: list[int]
    categoriesAttributes: list[str]
    screeningAttributes: list[str]
    contentLabels: list[str]
    languages: Languages
    originalLanguage: list[str]
    dubbedLanguage: list[str]
    firstSubbedLanguage: list[str]
    secondSubbedLanguage: list[str]


class Trailer(TypedDict):
    filmId: str
    filmName: str
    filmLink: str
    videoLink: str | None

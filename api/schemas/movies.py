import re
from datetime import date, datetime
from enum import StrEnum
from typing import Self

from pydantic import Field

from .. import cinemacity as cc
from ..schemas.common import ApiModel, Languages


class MovieStatus(StrEnum):
    SHOWING = 'showing'
    UPCOMING = 'upcoming'
    PAST = 'past'

    @classmethod
    def from_cinema_city(cls, showing_type: cc.schemas.film.FilmShowingType) -> Self:
        return cls(_STATUS_BY_SHOWING_TYPE[showing_type])

    def to_cinema_city(self) -> cc.schemas.film.FilmShowingType:
        return _SHOWING_TYPE_BY_STATUS[self]


_SHOWING_TYPE_BY_STATUS: dict[MovieStatus, cc.schemas.film.FilmShowingType] = {
    MovieStatus.SHOWING: 'SHOWING',
    MovieStatus.UPCOMING: 'FUTURE',
    MovieStatus.PAST: 'PAST',
}
_STATUS_BY_SHOWING_TYPE = {v: k for k, v in _SHOWING_TYPE_BY_STATUS.items()}


class Movie(ApiModel):
    id: str = Field(examples=['7803s2r'])
    title: str = Field(examples=['Igrzyska śmierci: Wschód słońca w dniu dożynek'])
    poster_url: str
    trailer_url: str | None
    website_url: str = Field(description='Movie page on the Cinema City website.')
    release_date: date | None
    duration_minutes: int | None = Field(
        description='Not available in movie listings, only for bookable movies.'
    )
    attributes: list[str] = Field(
        description='Genres, formats and language versions, e.g. `action`, `4dx`.',
        examples=[['2d', 'action', 'dubbed']],
    )
    languages: Languages

    @classmethod
    def from_poster(cls, poster: cc.schemas.film.Poster) -> Self:
        trailer_urls = (m['url'] for m in poster['mediaList'] if m['type'] == 'Video')
        return cls(
            id=poster['code'],
            title=poster['featureTitle'],
            poster_url=poster['posterSrc'],
            trailer_url=next(trailer_urls, None),
            website_url=poster['url'],
            release_date=_parse_date(poster['dateStarted']),
            duration_minutes=None,
            attributes=poster['attributes'],
            languages=Languages.from_cinema_city(poster['languages']),
        )

    @classmethod
    def from_film(cls, film: cc.schemas.film.Film) -> Self:
        return cls(
            id=film['id'],
            title=film['name'],
            poster_url=film['posterLink'],
            trailer_url=film['videoLink'],
            website_url=film['link'],
            release_date=_parse_date(film['releaseDate']),
            duration_minutes=film['length'],
            attributes=film['attributeIds'],
            languages=Languages.from_cinema_city(film['languages']),
        )


class AgeRating(ApiModel):
    code: str = Field(examples=['15-plus'])
    icon_url: str


class MovieDetails(Movie):
    original_title: str
    status: MovieStatus
    synopsis: str
    cast: list[str]
    directors: list[str]
    release_year: int | None
    release_country: str | None
    genres: list[str] = Field(examples=[['action', 'thriller']])
    age_rating: AgeRating
    screening_count: int = Field(description='Number of scheduled screenings.')

    @classmethod
    def from_cinema_city(cls, details: cc.schemas.film.FilmDetails) -> Self:
        release_year = details['releaseYear']
        return cls(
            id=details['id'],
            title=details['name'],
            original_title=details['originalName'],
            status=MovieStatus.from_cinema_city(details['showingType']),
            poster_url=details['posterLinkLarge'],
            trailer_url=details['videoLink'],
            website_url=details['link'],
            release_date=_parse_date(details['dateStarted']),
            release_year=int(release_year) if release_year else None,
            release_country=details['releaseCountry'],
            duration_minutes=details['length'],
            synopsis=details['synopsis'],
            cast=_split_names(details['cast']),
            directors=_split_names(details['directors']),
            genres=details['categoriesAttributes'],
            attributes=details['screeningAttributes'] + details['categoriesAttributes'],
            languages=Languages.from_cinema_city(details['languages']),
            age_rating=AgeRating(
                code=details['ageRestrictionName'],
                icon_url=details['ageRestrictionLink'],
            ),
            screening_count=details['eventCount'],
        )


class Trailer(ApiModel):
    movie_id: str
    movie_title: str
    movie_url: str = Field(description='Movie page on the Cinema City website.')
    video_url: str | None

    @classmethod
    def from_cinema_city(cls, trailer: cc.schemas.film.Trailer) -> Self:
        return cls(
            movie_id=trailer['filmId'],
            movie_title=trailer['filmName'],
            movie_url=trailer['filmLink'],
            video_url=trailer['videoLink'],
        )


def _parse_date(value: str) -> datetime.date:
    return datetime.fromisoformat(value).date()


def _split_names(names: str | None) -> list[str]:
    """Split a comma and/or newline separated list."""
    if not names:
        return []
    return [name.strip() for name in re.split(r'[,\n]', names) if name.strip()]

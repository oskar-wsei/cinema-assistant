from collections import defaultdict
from collections.abc import Callable
from datetime import date, datetime
from operator import attrgetter
from typing import Self

from pydantic import Field

from .. import cinemacity as cc
from ..schemas.cinemas import Cinema
from ..schemas.common import ApiModel, Languages
from ..schemas.movies import Movie


class Screening(ApiModel):
    id: str = Field(examples=['1789206'])
    movie_id: str = Field(examples=['7803s2r'])
    cinema_id: str = Field(examples=['1064'])
    starts_at: datetime = Field(description="Start time in the cinema's local time.")
    business_date: date = Field(
        description='Cinema business day; late-night screenings belong to the '
        'previous day.'
    )
    auditorium: str = Field(examples=['Sala 5 - Milka'])
    attributes: list[str] = Field(examples=[['2d', 'dubbed']])
    languages: Languages
    seat_availability: float = Field(
        ge=0, le=1, description='Fraction of seats still available.'
    )
    sold_out: bool
    booking_url: str

    @classmethod
    def from_cinema_city(cls, event: cc.schemas.screening.Event) -> Self:
        return cls(
            id=event['id'],
            movie_id=event['filmId'],
            cinema_id=event['cinemaId'],
            starts_at=datetime.fromisoformat(event['eventDateTime']),
            business_date=date.fromisoformat(event['businessDay']),
            auditorium=event['auditorium'],
            attributes=event['attributeIds'],
            languages=Languages.from_cinema_city(event['languages']),
            seat_availability=event['availabilityRatio'],
            sold_out=event['soldOut'],
            booking_url=event['bookingLink'],
        )


class CinemaScreenings(ApiModel):
    """A cinema together with its screenings of the requested movie."""

    cinema: Cinema
    screenings: list[Screening]

    @classmethod
    def group(cls, cinema_events: cc.schemas.screening.CinemaEvents) -> list[Self]:
        screenings = _group_screenings(cinema_events['events'], attrgetter('cinema_id'))
        return [
            cls(
                cinema=Cinema.from_cinema_city(cinema),
                screenings=screenings[cinema['id']],
            )
            for cinema in cinema_events['cinemas']
        ]


class MovieScreenings(ApiModel):
    """A movie together with its screenings in the requested cinema."""

    movie: Movie
    screenings: list[Screening]

    @classmethod
    def group(cls, film_events: cc.schemas.screening.FilmEvents) -> list[Self]:
        screenings = _group_screenings(film_events['events'], attrgetter('movie_id'))
        return [
            cls(movie=Movie.from_film(film), screenings=screenings[film['id']])
            for film in film_events['films']
        ]


class PresaleMovie(ApiModel):
    """A not yet released movie with screenings already open for booking."""

    movie: Movie
    screening_dates: list[date]

    @classmethod
    def from_cinema_city(
        cls, presales: cc.schemas.screening.PresaleFilms
    ) -> list[Self]:
        dates_by_film_id = presales['eventsDatesByFilmId']
        return [
            cls(
                movie=Movie.from_film(film),
                screening_dates=[
                    date.fromisoformat(day)
                    for day in dates_by_film_id.get(film['id'], [])
                ],
            )
            for film in presales['films']
        ]


def _group_screenings(
    events: list[cc.schemas.screening.Event], key: Callable[[Screening], str]
) -> defaultdict[str, list[Screening]]:
    """Group events into chronologically sorted screenings by ``key``."""
    screenings = sorted(
        map(Screening.from_cinema_city, events), key=attrgetter('starts_at')
    )
    grouped: defaultdict[str, list[Screening]] = defaultdict(list)
    for screening in screenings:
        grouped[key(screening)].append(screening)
    return grouped

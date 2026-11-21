from collections.abc import Iterable
from datetime import date

import requests

from .base import CinemaCityClientBase
from .contract import (
    CinemaBody,
    CinemasBody,
    FilmDetailsBody,
    FilmsBody,
    GroupsBody,
    PostersBody,
)
from .default import (
    DEFAULT_BASE_URL,
    DEFAULT_TENANT_ID,
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_USER_AGENT,
)
from .schemas.attribute import AttributesConfig
from .schemas.cinema import Cinema, CinemaGroup
from .schemas.film import (
    FeedName,
    Film,
    FilmDetails,
    Poster,
    PosterShowingType,
    Trailer,
)
from .schemas.screening import CinemaEvents, FilmEvents, PresaleFilms


class CinemaCityClient(CinemaCityClientBase):
    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        tenant_id: str = DEFAULT_TENANT_ID,
        language: str | None = None,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        user_agent: str = DEFAULT_USER_AGENT,
        session: requests.Session | None = None,
    ) -> None:
        self._base_url = base_url.rstrip('/')
        self._tenant_id = tenant_id
        self._language = language
        self._timeout = timeout
        self._owns_session = session is None
        self._session = session or requests.Session()
        self._session.headers['User-Agent'] = user_agent

    def close(self) -> None:
        """Close the underlying session if it was created by this client."""
        if self._owns_session:
            self._session.close()

    def get_feed_names(self) -> list[FeedName]:
        """List the curated feeds available, e.g. ``"now-playing"``."""
        feed_names: list[FeedName] = self._get(f'feed/{self._tenant_id}/allFeedNames')
        return feed_names

    def get_feed(self, name: str) -> list[Poster]:
        """Get the films of a curated feed, see :meth:`get_feed_names`."""
        body: PostersBody = self._get(f'feed/{self._tenant_id}/byName/{name}')
        return body['posters']

    def get_now_playing(self) -> list[Poster]:
        """Get the films currently featured as playing in cinemas."""
        return self.get_feed('now-playing')

    def get_coming_soon(self) -> list[Poster]:
        """Get the films featured as coming soon."""
        return self.get_feed('coming-soon')

    def get_posters(
        self,
        showing_type: PosterShowingType = 'SHOWING',
        *,
        cinema_id: str | None = None,
        attributes: Iterable[str] | None = None,
    ) -> list[Poster]:
        """Get all films with the given showing status (not just featured ones)."""
        params = self._compact_params(
            cinemaId=cinema_id, attr=self._join_or_none(attributes)
        )
        body: PostersBody = self._get(
            f'poster/{self._tenant_id}/by-showing-type/{showing_type}', params
        )
        return body['posters']

    def get_films(
        self, *, until: date | None = None, attributes: Iterable[str] | None = None
    ) -> list[Film]:
        """Get the films that can be booked, with screenings up to ``until``."""
        body: FilmsBody = self._get(
            f'quickbook/{self._tenant_id}/films/until/{self._until(until)}',
            self._compact_params(attr=self._join_or_none(attributes)),
        )
        return body['films']

    def get_film_details(self, film_id: str) -> FilmDetails | None:
        """Get the details of a film, or ``None`` if it does not exist."""
        body: FilmDetailsBody | None = self._get_optional(
            f'{self._tenant_id}/films/byDistributorCode/{film_id}'
        )
        return body['filmDetails'] if body else None

    def get_trailers_in_cinema(self, cinema_id: str) -> list[Trailer]:
        """Get the trailers of the films screened in a cinema."""
        trailers: list[Trailer] = self._get(
            f'{self._tenant_id}/trailers/byCinemaId/{cinema_id}'
        )
        return trailers

    def get_cinemas(
        self, *, until: date | None = None, attributes: Iterable[str] | None = None
    ) -> list[Cinema]:
        """Get the cinemas that have screenings up to ``until``."""
        body: CinemasBody = self._get(
            f'quickbook/{self._tenant_id}/cinemas/with-event/until/{self._until(until)}',
            self._compact_params(attr=self._join_or_none(attributes)),
        )
        return body['cinemas']

    def get_cinema(self, cinema_id: str) -> Cinema | None:
        """Get a cinema by id, or ``None`` if it does not exist."""
        body: CinemaBody | None = self._get_optional(
            f'{self._tenant_id}/cinema/{cinema_id}'
        )
        return body['cinema'] if body else None

    def get_cinema_groups_with_film(
        self,
        film_id: str,
        *,
        until: date | None = None,
        attributes: Iterable[str] | None = None,
    ) -> list[CinemaGroup]:
        """Get the cinema groups (cities) where a film is screened."""
        body: GroupsBody = self._get(
            f'quickbook/{self._tenant_id}/groups/with-film/{film_id}'
            f'/until/{self._until(until)}',
            self._compact_params(attr=self._join_or_none(attributes)),
        )
        return body['groups']

    def get_dates_in_cinema(
        self,
        cinema_id: str,
        *,
        until: date | None = None,
        attributes: Iterable[str] | None = None,
    ) -> list[date]:
        """Get the days with any screenings in a cinema."""
        return self._get_dates(
            f'quickbook/{self._tenant_id}/dates/in-cinema/{cinema_id}'
            f'/until/{self._until(until)}',
            self._compact_params(attr=self._join_or_none(attributes)),
        )

    def get_dates_for_film_in_group(
        self,
        group_id: str,
        film_id: str,
        *,
        until: date | None = None,
        attributes: Iterable[str] | None = None,
    ) -> list[date]:
        """Get the days on which a film is screened in a cinema group (city)."""
        return self._get_dates(
            f'quickbook/{self._tenant_id}/dates/in-group/{group_id}'
            f'/with-film/{film_id}/until/{self._until(until)}',
            self._compact_params(attr=self._join_or_none(attributes)),
        )

    def get_dates_for_film_in_cinemas(
        self,
        film_id: str,
        cinema_ids: Iterable[str],
        *,
        until: date | None = None,
        attributes: Iterable[str] | None = None,
    ) -> list[date]:
        """Get the days on which a film is screened in any of the given cinemas."""
        return self._get_dates(
            f'quickbook/{self._tenant_id}/dates/with-film/{film_id}'
            f'/until/{self._until(until)}',
            self._compact_params(
                ids=','.join(cinema_ids), attr=self._join_or_none(attributes)
            ),
        )

    def get_film_events_in_cinema(
        self,
        cinema_id: str,
        at_date: date,
        *,
        attributes: Iterable[str] | None = None,
    ) -> FilmEvents:
        """Get all screenings in a cinema on a given day."""
        film_events: FilmEvents = self._get(
            f'quickbook/{self._tenant_id}/film-events/in-cinema/{cinema_id}'
            f'/at-date/{at_date.isoformat()}',
            self._compact_params(attr=self._join_or_none(attributes)),
        )
        return film_events

    def get_cinema_events_for_film_in_group(
        self,
        group_id: str,
        film_id: str,
        at_date: date,
        *,
        attributes: Iterable[str] | None = None,
    ) -> CinemaEvents:
        """Get the screenings of a film in a cinema group (city) on a given day."""
        cinema_events: CinemaEvents = self._get(
            f'quickbook/{self._tenant_id}/cinema-events/in-group/{group_id}'
            f'/with-film/{film_id}/at-date/{at_date.isoformat()}',
            self._compact_params(attr=self._join_or_none(attributes)),
        )
        return cinema_events

    def get_cinema_events_for_film_in_cinemas(
        self,
        film_id: str,
        cinema_ids: Iterable[str],
        at_date: date,
        *,
        attributes: Iterable[str] | None = None,
    ) -> CinemaEvents:
        """Get the screenings of a film in the given cinemas on a given day."""
        cinema_events: CinemaEvents = self._get(
            f'quickbook/{self._tenant_id}/cinema-events/with-film/{film_id}'
            f'/at-date/{at_date.isoformat()}',
            self._compact_params(
                ids=','.join(cinema_ids), attr=self._join_or_none(attributes)
            ),
        )
        return cinema_events

    def get_presale_films_in_cinema(
        self,
        cinema_id: str,
        as_at_date: date,
        *,
        attributes: Iterable[str] | None = None,
    ) -> PresaleFilms:
        """Get films premiering after ``as_at_date`` that already have screenings."""
        presale_films: PresaleFilms = self._get(
            f'quickbook/{self._tenant_id}/film-events-dates/in-cinema/{cinema_id}'
            f'/as-at-date/{as_at_date.isoformat()}',
            self._compact_params(attr=self._join_or_none(attributes)),
        )
        return presale_films

    def get_attributes(self) -> AttributesConfig:
        """Get the attributes (genres, formats, languages...) usable as filters."""
        attributes: AttributesConfig = self._get(
            f'quickbook/{self._tenant_id}/attributes'
        )
        return attributes

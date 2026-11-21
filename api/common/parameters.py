"""Reusable, documented path and query parameters."""

from datetime import date
from typing import Annotated

from fastapi import Path, Query

CinemaIdPath = Annotated[
    str, Path(description='Cinema id, see `GET /cinemas`.', examples=['1064'])
]
CityIdPath = Annotated[
    str, Path(description='City id, see `GET /cities`.', examples=['krakow'])
]
MovieIdPath = Annotated[
    str, Path(description='Movie id, see `GET /movies`.', examples=['7803s2r'])
]
FeedNamePath = Annotated[
    str, Path(description='Feed name, see `GET /feeds`.', examples=['now-playing'])
]

AttributesQuery = Annotated[
    list[str] | None,
    Query(
        alias='attribute',
        description=(
            'Only include results with this attribute, e.g. a format (`4dx`, `imax`) '
            'or language version (`dubbed`). Repeatable. See `GET /attributes`.'
        ),
    ),
]
UntilQuery = Annotated[
    date | None,
    Query(description='Last day to include. Defaults to a year from today.'),
]
DateQuery = Annotated[
    date | None,
    Query(alias='date', description='Day of the screenings. Defaults to today.'),
]

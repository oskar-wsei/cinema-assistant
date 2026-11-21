from typing import Self

from pydantic import Field

from .. import cinemacity as cc
from ..schemas.common import ApiModel


class Feed(ApiModel):
    name: str = Field(examples=['now-playing'])
    placements: dict[str, int] = Field(
        description='Website page name mapped to the position of the feed on it.',
        examples=[{'home': 0}],
    )

    @classmethod
    def from_cinema_city(cls, feed: cc.schemas.film.FeedName) -> Self:
        return cls(name=feed['key'], placements=feed['placements'])

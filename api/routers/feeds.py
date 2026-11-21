from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..common.dependencies import ClientDep
from ..common.errors import NOT_FOUND_RESPONSE, UPSTREAM_ERROR_RESPONSE
from ..common.parameters import FeedNamePath
from ..schemas.feeds import Feed
from ..schemas.movies import Movie

router = APIRouter(prefix='/feeds', tags=['Feeds'], responses=UPSTREAM_ERROR_RESPONSE)


def get_feeds(client: ClientDep) -> list[Feed]:
    return [Feed.from_cinema_city(feed) for feed in client.get_feed_names()]


FeedsDep = Annotated[list[Feed], Depends(get_feeds)]


def get_feed_or_404(feed_name: FeedNamePath, feeds: FeedsDep) -> Feed:
    feed = next((feed for feed in feeds if feed.name == feed_name), None)
    if feed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Feed {feed_name!r} not found.',
        )
    return feed


ExistingFeed = Annotated[Feed, Depends(get_feed_or_404)]


@router.get('', summary='List feeds')
def list_feeds(feeds: FeedsDep) -> list[Feed]:
    return feeds


@router.get('/{feed_name}', summary='Get a feed', responses=NOT_FOUND_RESPONSE)
def get_feed(feed: ExistingFeed) -> Feed:
    return feed


@router.get(
    '/{feed_name}/movies',
    summary='List movies in a feed',
    responses=NOT_FOUND_RESPONSE,
)
def list_feed_movies(feed: ExistingFeed, client: ClientDep) -> list[Movie]:
    return [Movie.from_poster(poster) for poster in client.get_feed(feed.name)]

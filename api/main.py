from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import requests
import requests_cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .cinemacity.client import CinemaCityClient
from .common.config import Settings, get_settings
from .common.errors import register_exception_handlers
from .routers import attributes, cinemas, cities, feeds, health, movies

DESCRIPTION = """
Read-only Restful API for [Cinema City](https://www.cinema-city.pl).
"""

TAGS_METADATA = [
    {'name': 'Movies', 'description': 'Movies, their details and screenings.'},
    {'name': 'Cinemas', 'description': 'Cinemas and what they screen.'},
    {'name': 'Cities', 'description': 'Cities with Cinema City cinemas.'},
    {'name': 'Feeds', 'description': 'Curated movie lists from the website.'},
    {'name': 'Attributes', 'description': 'Values for `attribute` filters.'},
    {'name': 'Health', 'description': 'Service health.'},
]


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        with (
            _create_session(settings) as session,
            CinemaCityClient(
                base_url=settings.base_url,
                tenant_id=settings.tenant_id,
                language=settings.language,
                timeout=settings.timeout_seconds,
                session=session,
            ) as client,
        ):
            app.state.client = client
            yield

    app = FastAPI(
        title='Cinema City API',
        version='1.0.0',
        description=DESCRIPTION,
        openapi_tags=TAGS_METADATA,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=['GET'],
        allow_headers=['*'],
    )
    register_exception_handlers(app)
    app.include_router(movies.router)
    app.include_router(cinemas.router)
    app.include_router(cities.router)
    app.include_router(feeds.router)
    app.include_router(attributes.router)
    app.include_router(health.router)
    return app


def _create_session(settings: Settings) -> requests.Session:
    if settings.cache_ttl_seconds == 0:
        return requests.Session()
    return requests_cache.CachedSession(
        backend='memory', expire_after=settings.cache_ttl_seconds
    )


app = create_app()

from collections.abc import Iterator

import pytest
import requests_mock
from api.cinemacity.client import CinemaCityClient
from api.common.config import Settings
from api.main import create_app
from fastapi.testclient import TestClient

from tests.upstream import BASE_URL, TENANT_ID, FakeCinemaCity


@pytest.fixture
def upstream() -> Iterator[FakeCinemaCity]:
    with requests_mock.Mocker(case_sensitive=True) as mocker:
        fake = FakeCinemaCity(mocker)
        yield fake
        fake.assert_all_stubs_requested()


@pytest.fixture
def settings() -> Settings:
    return Settings(
        _env_file=None,
        base_url=BASE_URL,
        tenant_id=TENANT_ID,
        language=None,
        cache_ttl_seconds=0,
    )


@pytest.fixture
def api(settings: Settings, upstream: FakeCinemaCity) -> Iterator[TestClient]:
    """The real application, talking to the fake Cinema City API."""
    with TestClient(create_app(settings)) as client:
        yield client


@pytest.fixture
def cinema_city(upstream: FakeCinemaCity) -> Iterator[CinemaCityClient]:
    with CinemaCityClient(base_url=BASE_URL, tenant_id=TENANT_ID) as client:
        yield client

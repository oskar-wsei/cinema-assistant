from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Protocol
from urllib.parse import urlencode

import requests_mock
from api.cinemacity.default import DEFAULT_DAYS_AHEAD

BASE_URL = 'https://cinema-city.test/data-api-service/v1'
TENANT_ID = '10103'
TODAY = date.today().isoformat()
DEFAULT_UNTIL = (date.today() + timedelta(days=DEFAULT_DAYS_AHEAD)).isoformat()


class _Stub(Protocol):
    @property
    def called(self) -> bool: ...


class FakeCinemaCity:
    """Fake Cinema City API asserting the exact URLs the client requests.

    Each stub matches only its exact path and complete query string, so
    registering a stub is an assertion on how the request URL is built:

    * a request matching no stub fails the test, naming the unexpected URL,
    * :meth:`assert_all_stubs_requested` fails for stubs that were never used.
    """

    def __init__(self, mocker: requests_mock.Mocker) -> None:
        self._mocker = mocker
        self._stubs: dict[str, _Stub] = {}
        mocker.get(requests_mock.ANY, json=_fail_on_unexpected_request)

    def stub(
        self,
        path: str,
        body: object = None,
        *,
        query: dict[str, str] | None = None,
        status_code: int = 200,
        **response: Any,
    ) -> None:
        """Respond to ``GET {BASE_URL}/{path}?{query}`` with ``{"body": body}``.

        Without ``body``, ``requests_mock`` response options (``json``,
        ``text``, ``exc``...) can be passed instead, e.g. to simulate errors.
        """
        url = f'{BASE_URL}/{path}'
        if query:
            url = f'{url}?{urlencode(query)}'
        if body is not None:
            response['json'] = {'body': body}
        if 'exc' not in response:  # requests_mock rejects a status with ``exc``.
            response['status_code'] = status_code
        self._stubs[url] = self._mocker.get(url, complete_qs=True, **response)

    @property
    def request_count(self) -> int:
        return len(self._mocker.request_history)

    @property
    def last_request(self) -> requests_mock.Request:
        request = self._mocker.last_request
        assert request is not None, 'No request was sent to Cinema City.'
        return request

    def assert_all_stubs_requested(self) -> None:
        unused = [url for url, stub in self._stubs.items() if not stub.called]
        assert not unused, f'Stubbed but never requested: {unused}'


def _fail_on_unexpected_request(
    request: requests_mock.Request, context: requests_mock.Context
) -> None:
    raise AssertionError(f'Unexpected Cinema City request: GET {request.url}')

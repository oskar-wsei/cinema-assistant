from collections.abc import Iterable
from datetime import date, timedelta
from http import HTTPStatus
from types import TracebackType
from typing import Any, Self

import requests

from .contract import DatesBody, QueryParams
from .default import DEFAULT_DAYS_AHEAD
from .error import CinemaCityAPIError, CinemaCityError


class CinemaCityClientBase:
    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def _get_dates(self, path: str, params: QueryParams) -> list[date]:
        body: DatesBody = self._get(path, params)
        return [date.fromisoformat(day) for day in body['dates']]

    def _get(self, path: str, params: QueryParams | None = None) -> Any:
        """Fetch ``path`` and return the unwrapped ``body`` of the response."""
        body = self._get_optional(path, params)
        if body is None:
            raise CinemaCityError(f'Unexpected empty response for {path!r}')
        return body

    def _get_optional(self, path: str, params: QueryParams | None = None) -> Any:
        """Like :meth:`_get`, but return ``None`` on ``204 No Content``.

        The API answers lookups of non-existent resources with 204.
        """
        query = dict(params or {})
        if self._language:
            query['lang'] = self._language
        try:
            response = self._session.get(
                f'{self._base_url}/{path}', params=query, timeout=self._timeout
            )
        except requests.RequestException as exc:
            raise CinemaCityError(f'Request to {path!r} failed: {exc}') from exc

        if not response.ok:
            raise CinemaCityAPIError.from_response(response)
        if response.status_code == HTTPStatus.NO_CONTENT:
            return None
        try:
            return response.json()['body']
        except (requests.JSONDecodeError, KeyError, TypeError) as exc:
            raise CinemaCityError(f'Malformed response for {path!r}') from exc

    @staticmethod
    def _until(until: date | None) -> str:
        return (until or date.today() + timedelta(days=DEFAULT_DAYS_AHEAD)).isoformat()

    @staticmethod
    def _join_or_none(values: Iterable[str] | None) -> str | None:
        return ','.join(values) if values is not None else None

    @staticmethod
    def _compact_params(**params: str | None) -> dict[str, str]:
        return {key: value for key, value in params.items() if value is not None}

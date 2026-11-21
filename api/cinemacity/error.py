from http import HTTPStatus

import requests


class CinemaCityError(Exception): ...


class CinemaCityAPIError(CinemaCityError):
    def __init__(
        self, status_code: int, message: str, message_code: str | None = None
    ) -> None:
        super().__init__(f'HTTP {status_code}: {message}')
        self.status_code = status_code
        self.message = message
        self.message_code = message_code

    @classmethod
    def from_response(cls, response: requests.Response) -> 'CinemaCityAPIError':
        reason = cls._reason_phrase(response)
        try:
            payload = response.json()
        except requests.JSONDecodeError:
            # E.g. HTML error page
            payload = None
        if not isinstance(payload, dict):
            return cls(response.status_code, reason)
        return cls(
            response.status_code,
            str(payload.get('message', reason)),
            payload.get('messageCode'),
        )

    @staticmethod
    def _reason_phrase(response: requests.Response) -> str:
        if response.reason:
            return response.reason
        try:
            return HTTPStatus(response.status_code).phrase
        except ValueError:
            return 'Unknown error'

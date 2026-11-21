from typing import Final

DEFAULT_BASE_URL: Final = 'https://www.cinema-city.pl/pl/data-api-service/v1'
DEFAULT_TENANT_ID: Final = '10103'  # Poland
DEFAULT_USER_AGENT: Final = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
)  # Cinema City requires sensible User-Agent or requests may be blocked
DEFAULT_TIMEOUT_SECONDS: Final = 10.0
DEFAULT_DAYS_AHEAD: Final = 365

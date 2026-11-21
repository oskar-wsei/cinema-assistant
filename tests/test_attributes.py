from fastapi.testclient import TestClient

from .upstream import FakeCinemaCity


def test_list_attributes(api: TestClient, upstream: FakeCinemaCity) -> None:
    upstream.stub(
        'quickbook/10103/attributes',
        {
            'attributes': [
                {
                    'group-name': 'screening-type',
                    'items': [
                        {
                            'id': '4dx',
                            'url': 'https://example.com/4dx.png',
                            'visible': True,
                            'sequence': None,
                        },
                        {'id': '2d', 'url': None, 'visible': False, 'sequence': None},
                    ],
                }
            ],
            'dropdownConfig': {'genres': [], 'screening-type': [], 'other': []},
            'mobileFilterConfig': [],
        },
    )

    response = api.get('/attributes')

    assert response.json() == [
        {
            'name': 'screening-type',
            'attributes': [
                {
                    'id': '4dx',
                    'icon_url': 'https://example.com/4dx.png',
                    'visible': True,
                },
                {'id': '2d', 'icon_url': None, 'visible': False},
            ],
        }
    ]

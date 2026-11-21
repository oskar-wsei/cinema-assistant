"""Builders of Cinema City API payloads with sensible defaults."""

import api.cinemacity as cc

LANGUAGES: cc.schemas.common.Languages = {
    'original': ['en'],
    'dubbed': ['pl'],
    'voiceover': [],
    'subtitles': ['pl'],
}


def make_poster(code: str = '7803s2r', title: str = 'Movie') -> cc.schemas.film.Poster:
    return {
        'code': code,
        'featureTitle': title,
        'url': f'https://example.com/filmy/{code}',
        'posterSrc': f'https://example.com/posters/{code}.jpg',
        'weight': 0,
        'dateStarted': '2026-11-20T00:00:00',
        'filmShowingType': 'SHOWING',
        'attributes': ['2d', 'action'],
        'languages': LANGUAGES,
        'mediaList': [
            {
                'type': 'Image',
                'subType': 'md',
                'url': f'https://example.com/posters/{code}-md.jpg',
                'dimensionWidth': '220',
                'dimensionHeight': '326',
            },
            {
                'type': 'Video',
                'subType': '',
                'url': 'https://youtube.com/watch?v=trailer',
                'dimensionWidth': None,
                'dimensionHeight': None,
            },
        ],
    }


def make_film(film_id: str = '7803s2r', name: str = 'Movie') -> cc.schemas.film.Film:
    return {
        'id': film_id,
        'name': name,
        'length': 158,
        'posterLink': f'https://example.com/posters/{film_id}.jpg',
        'videoLink': None,
        'link': f'https://example.com/filmy/{film_id}',
        'weight': 0,
        'releaseYear': '2026',
        'releaseDate': '2026-11-20T00:00:00',
        'attributeIds': ['2d'],
        'languages': LANGUAGES,
    }


def make_film_details(film_id: str = '7803s2r') -> cc.schemas.film.FilmDetails:
    return {
        'id': film_id,
        'name': 'Igrzyska śmierci',
        'originalName': 'The Hunger Games',
        'length': 158,
        'synopsis': 'Synopsis.',
        'cast': 'Joseph Zada, Elle Fanning,\nJesse Plemons',
        'directors': 'Francis Lawrence',
        'releaseYear': '2026',
        'releaseCountry': 'USA',
        'dateStarted': '2026-11-20T00:00:00',
        'showingType': 'FUTURE',
        'weight': 0,
        'eventCount': 42,
        'link': f'https://example.com/filmy/{film_id}',
        'posterLink': f'https://example.com/posters/{film_id}.jpg',
        'posterLinkLarge': f'https://example.com/posters/{film_id}-lg.jpg',
        'videoLink': 'https://youtube.com/watch?v=trailer',
        'mediaList': [],
        'distributorName': None,
        'specialMessage': None,
        'ageRestrictionId': 6,
        'ageRestrictionName': '15-plus',
        'ageRestrictionLink': 'https://example.com/rating/15.png',
        'ageRestrictionDescription': None,
        'categoryIds': [4],
        'categoriesAttributes': ['action'],
        'screeningAttributes': ['2d', 'imax'],
        'contentLabels': [],
        'languages': LANGUAGES,
        'originalLanguage': ['original-lang-en'],
        'dubbedLanguage': ['dubbed-lang-pl'],
        'firstSubbedLanguage': ['first-subbed-lang-pl'],
        'secondSubbedLanguage': [],
    }


def make_cinema(
    cinema_id: str = '1064', group_id: str = 'krakow', city: str = 'Kraków'
) -> cc.schemas.cinema.Cinema:
    return {
        'id': cinema_id,
        'groupId': group_id,
        'displayName': f'{city} - {cinema_id}',
        'link': f'https://example.com/kina/{cinema_id}',
        'imageUrl': f'https://example.com/kina/{cinema_id}.jpg',
        'address': 'ul. Zakopiańska 62, https://example.com/map',
        'addressInfo': {
            'address1': 'ul. Zakopiańska 62',
            'address2': None,
            'address3': None,
            'address4': None,
            'city': city,
            'state': None,
            'postalCode': '30-418',
        },
        'latitude': 50.01654,
        'longitude': 19.930508,
        'bookingUrl': None,
        'blockOnlineSales': False,
        'blockOnlineSalesUntil': None,
    }


def make_cinema_with_events(
    cinema_id: str = '1064',
) -> cc.schemas.cinema.CinemaWithEvents:
    return {**make_cinema(cinema_id), 'attributeIds': ['2d'], 'languages': LANGUAGES}


def make_event(
    event_id: str,
    *,
    film_id: str = '7803s2r',
    cinema_id: str = '1064',
    starts_at: str = '2026-11-20T18:00:00',
) -> cc.schemas.screening.Event:
    return {
        'id': event_id,
        'filmId': film_id,
        'cinemaId': cinema_id,
        'businessDay': starts_at[:10],
        'eventDateTime': starts_at,
        'auditorium': 'Sala 1',
        'auditoriumTinyName': 'S01',
        'availabilityRatio': 0.75,
        'soldOut': False,
        'presentationCode': event_id,
        'attributeIds': ['2d'],
        'languages': LANGUAGES,
        'bookingLink': f'https://example.com/order/{event_id}',
        'bookingRouterLaunchLink': f'https://example.com/launch/{event_id}',
        'compositeBookingLink': {
            'type': 'PG',
            'bookingUrl': {
                'url': f'https://example.com/order/{event_id}',
                'params': {'lang': 'pl-PL'},
            },
            'obsoleteBookingUrl': f'https://example.com/order/{event_id}',
            'serviceUrl': 'https://example.com/booking',
            'blockOnlineSales': False,
            'blockOnlineSalesUntil': None,
        },
    }

from api.schemas.cinemas import City

from .factories import make_cinema


def test_city_is_named_after_the_town_most_of_its_cinemas_are_in() -> None:
    cinemas = [
        make_cinema('1062', 'katowice', 'Bytom'),
        make_cinema('1063', 'katowice', 'Katowice'),
        make_cinema('1065', 'katowice', 'Katowice'),
    ]

    [city] = City.from_cinemas(cinemas)

    assert city.name == 'Katowice'
    assert city.cinema_ids == ['1062', '1063', '1065']

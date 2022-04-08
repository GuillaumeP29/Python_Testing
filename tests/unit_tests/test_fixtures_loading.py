from server import load_clubs, load_competitions


def test_load_clubs_should_return_list():
    clubs = load_clubs()
    assert isinstance(clubs, list)


def test_load_clubs_should_return_dicts():
    clubs = load_clubs()
    assert isinstance(clubs[0], dict)


def test_load_clubs_should_return_at_least_one_club():
    clubs = load_clubs()
    assert clubs[0]['name'] is not None


def test_load_competitions_should_return_list():
    competitions = load_competitions()
    assert isinstance(competitions, list)


def test_load_competitions_should_return_dicts():
    competitions = load_competitions()
    assert isinstance(competitions[0], dict)


def test_load_competitions_should_return_at_least_one_competition():
    competitions = load_competitions()
    assert competitions[0]['name'] is not None

from server import loadClubs, loadCompetitions


def test_load_clubs_should_return_list():
    clubs = loadClubs()
    assert isinstance(clubs, list)


def test_load_clubs_should_return_dicts():
    clubs = loadClubs()
    assert isinstance(clubs[0], dict)


def test_load_clubs_should_return_at_least_one_club():
    clubs = loadClubs()
    assert clubs[0]['name'] is not None


def test_load_competitions_should_return_list():
    competitions = loadCompetitions()
    assert isinstance(competitions, list)


def test_load_competitions_should_return_dicts():
    competitions = loadCompetitions()
    assert isinstance(competitions[0], dict)


def test_load_competitions_should_return_at_least_one_competition():
    competitions = loadCompetitions()
    assert competitions[0]['name'] is not None

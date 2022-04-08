from flaskr.server import competitions, clubs

INITIAL_NB_OF_PLACES = 25
INITIAL_NB_OF_POINTS = 30
TEST_CLUB_NAME = 'test_club'
TEST_COMPETITION_NAME = 'test_competition'


def add_competition_for_tests():
    test_competition = {
        'name': TEST_COMPETITION_NAME,
        'date': '2023-03-27 10:00:00',
        'number_of_places': INITIAL_NB_OF_PLACES,
        'attending_clubs': {}
    }
    competitions.append(test_competition)


def add_club_for_tests():
    test_club = {
        'name': TEST_CLUB_NAME,
        'email': 'admin@test_club.com',
        'points': INITIAL_NB_OF_POINTS
    }
    clubs.append(test_club)


def reset_test_club_points():
    club = [c for c in clubs if c['name'] == 'test_club'][0]
    club['points'] = INITIAL_NB_OF_POINTS


def reset_test_competition_nb_of_places():
    competition = [c for c in competitions if c['name'] == 'test_competition'][0]
    competition['number_of_places'] = INITIAL_NB_OF_PLACES


def reset_test_club_attendees_to_test_competition():
    competition = [c for c in competitions if c['name'] == 'test_competition'][0]
    competition['attending_clubs']['test_club'] = 0


def set_10_test_club_attendees_to_test_competition():
    competition = [c for c in competitions if c['name'] == 'test_competition'][0]
    competition['attending_clubs']['test_club'] = 10

import pytest

from server import app
from tests.data_for_testing import (
    add_competition_for_tests, add_club_for_tests, reset_test_competition_nb_of_places, reset_test_club_points,
    TEST_COMPETITION_NAME, TEST_CLUB_NAME, INITIAL_NB_OF_PLACES, INITIAL_NB_OF_POINTS
    )


add_competition_for_tests()
add_club_for_tests()


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_purchase_places_should_decrease_nb_of_places(client):
    reset_test_competition_nb_of_places()
    nb_of_places_to_buy = 3
    new_nb_of_places_expected = INITIAL_NB_OF_PLACES - nb_of_places_to_buy
    client.post('/purchasePlaces/', data={
        'competition': TEST_COMPETITION_NAME, 'club': TEST_CLUB_NAME, 'places': nb_of_places_to_buy
        })
    response = client.get(f'/book/{TEST_COMPETITION_NAME}/{TEST_CLUB_NAME}/')
    p_to_find = f'<p>Places available: {new_nb_of_places_expected}</p>'
    assert p_to_find in str(response.data)


def test_purchase_places_should_decrease_nb_of_points(client):
    reset_test_club_points()
    nb_of_places_to_buy = 3
    points_per_place = 3
    new_nb_of_places_expected = INITIAL_NB_OF_POINTS - (nb_of_places_to_buy * points_per_place)
    client.post('/purchasePlaces/', data={
        'competition': TEST_COMPETITION_NAME, 'club': TEST_CLUB_NAME, 'places': nb_of_places_to_buy
        })
    response = client.post('/showSummary/', data={'email': 'admin@test_club.com'})
    p_to_find = f'<p>Points available: {new_nb_of_places_expected}</p>'
    assert p_to_find in str(response.data)

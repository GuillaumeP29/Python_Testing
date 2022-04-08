import pytest
from flask import get_flashed_messages

from flaskr.server import app
from tests.data_for_testing import (
    add_competition_for_tests, add_club_for_tests, reset_test_competition_nb_of_places,
    set_10_test_club_attendees_to_test_competition, reset_test_club_points,
    TEST_COMPETITION_NAME, TEST_CLUB_NAME, INITIAL_NB_OF_PLACES
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
    response = client.post('/purchase-places/', data={
        'competition': TEST_COMPETITION_NAME, 'club': TEST_CLUB_NAME, 'places': nb_of_places_to_buy
        })
    new_nb_of_places_expected = INITIAL_NB_OF_PLACES - nb_of_places_to_buy
    p_to_find = f'<p>Number of Places: {new_nb_of_places_expected}</p>'
    assert p_to_find in str(response.data)


def test_purchase_places_should_send_succes_message(client):
    nb_of_places_to_buy = 3
    client.post('/purchase-places/', data={
        'competition': TEST_COMPETITION_NAME, 'club': TEST_CLUB_NAME, 'places': nb_of_places_to_buy
        })
    message = get_flashed_messages()
    assert message[0] == f'Great - booking complete! - {nb_of_places_to_buy} places purchased'


def test_purchase_places_should_not_allow_more_than_12_places_per_club(client):
    reset_test_competition_nb_of_places()
    set_10_test_club_attendees_to_test_competition()
    nb_of_places_to_buy = 3
    response = client.post('/purchase-places/', data={
        'competition': TEST_COMPETITION_NAME, 'club': TEST_CLUB_NAME, 'places': nb_of_places_to_buy
        })
    p_to_find = f'<p>Number of Places: {INITIAL_NB_OF_PLACES}</p>'
    assert p_to_find in str(response.data)


def test_purchase_places_should_send_error_message_for_more_than_12_places_per_club(client):
    set_10_test_club_attendees_to_test_competition()
    reset_test_club_points()
    nb_of_places_to_buy = 3
    client.post('/purchase-places/', data={
        'competition': TEST_COMPETITION_NAME, 'club': TEST_CLUB_NAME, 'places': nb_of_places_to_buy
        })
    message = get_flashed_messages()
    assert message[0] == f'{TEST_CLUB_NAME} would have more than 12 places - booking refused!'

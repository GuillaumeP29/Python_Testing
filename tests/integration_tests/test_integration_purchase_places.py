import pytest
from flask import get_flashed_messages

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


def test_public_board_access_and_go_back_to_index_is_possible_for_everyone(client):
    response = client.get('/')
    if response.status_code == 200:
        response = client.get('/public-board/')
        if 'test_club' in str(response.data):
            response = client.get('/')
            assert response.status_code == 200
        else:
            assert False
    else:
        assert False


def test_purchase_places_should_decrease_nb_of_places(client):
    reset_test_competition_nb_of_places()
    nb_of_places_to_buy = 3
    new_nb_of_places_expected = INITIAL_NB_OF_PLACES - nb_of_places_to_buy
    client.post('/purchase-places/', data={
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
    client.post('/purchase-places/', data={
        'competition': TEST_COMPETITION_NAME, 'club': TEST_CLUB_NAME, 'places': nb_of_places_to_buy
        })
    response = client.post('/show-summary/', data={'email': 'admin@test_club.com'})
    p_to_find = f'<p>Points available: {new_nb_of_places_expected}</p>'
    assert p_to_find in str(response.data)


def test_book_on_finished_event_should_flash_specific_message(client):
    client.get(r'/book/Spring%20Festival/Simply%20Lift/')
    expected_message = 'You cannot purchase places for a competition which is already finished'
    message = get_flashed_messages()
    assert message[0] == expected_message

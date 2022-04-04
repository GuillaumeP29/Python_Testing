import pytest
from flask import get_flashed_messages

from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_purchase_places_should_decrease_nb_of_places(client):
    initial_nb_of_places = 19
    nb_of_places_to_buy = 3
    new_nb_of_places_expected = initial_nb_of_places - nb_of_places_to_buy
    response = client.post('/purchasePlaces/', data={
        'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': str(nb_of_places_to_buy)
        })
    p_to_find = f'<p>Number of Places: {new_nb_of_places_expected}</p>'
    assert p_to_find in str(response.data)


def test_purchase_places_should_send_succes_message(client):
    nb_of_places_to_buy = 3
    client.post('/purchasePlaces/', data={
        'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': str(nb_of_places_to_buy)
        })
    message = get_flashed_messages()
    assert message[0] == 'Great-booking complete!'


def test_purchase_places_should_not_allow_more_than_12_places_per_club(client):
    initial_nb_of_places = 13
    nb_of_places_to_buy = 3
    response = client.post('/purchasePlaces/', data={
        'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': str(nb_of_places_to_buy)
        })
    p_to_find = f'<p>Number of Places: {initial_nb_of_places}</p>'
    assert p_to_find in str(response.data)


def test_purchase_places_should_send_error_message_for_more_than_12_places_per_club(client):
    nb_of_places_to_buy = 3
    client.post('/purchasePlaces/', data={
        'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': str(nb_of_places_to_buy)
        })
    message = get_flashed_messages()
    assert message[0] == 'Simply Lift would have more than 12 places-booking refused!'

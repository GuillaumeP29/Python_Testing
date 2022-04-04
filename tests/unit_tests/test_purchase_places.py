import pytest

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

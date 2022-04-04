import pytest

from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_purchase_places_should_decrease_nb_of_places(client):
    initial_nb_of_places = 25
    nb_of_places_to_buy = 3
    new_nb_of_places_expected = initial_nb_of_places - nb_of_places_to_buy
    client.post('/purchasePlaces/', data={
        'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': str(nb_of_places_to_buy)
        })
    response = client.get(r'/book/Spring%20Festival/Simply%20Lift/')
    p_to_find = f'<p>Places available: {new_nb_of_places_expected}</p>'
    assert p_to_find in str(response.data)


def test_purchase_places_should_decrease_nb_of_points(client):
    initial_nb_of_points = 10
    nb_of_places_to_buy = 3
    new_nb_of_places_expected = initial_nb_of_points - nb_of_places_to_buy
    client.post('/purchasePlaces/', data={
        'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': str(nb_of_places_to_buy)
        })
    response = client.post('/showSummary/', data={'email': 'john@simplylift.co'})
    print("response.data : ")
    print(response.data)
    p_to_find = f'<p>Points available: {new_nb_of_places_expected}</p>'
    assert p_to_find in str(response.data)

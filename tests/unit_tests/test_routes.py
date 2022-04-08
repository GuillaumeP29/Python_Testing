import pytest

from flaskr.server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_index_should_status_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200


def test_post_show_summary_with_correct_email_should_status_code_ok(client):
    response = client.post('/show-summary/', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200


def test_post_show_summary_with_wrong_email_should_redirect_to_index(client):
    response = client.post('/show-summary/', data={'email': 'fake@email.com'})
    assert response.status_code == 302


def test_post_show_summary_with_empty_email_should_redirect_to_index(client):
    response = client.post('/show-summary/', data={'email': ''})
    assert response.status_code == 302


def test_get_show_summary_should_should_redirect_to_index(client):
    response = client.get('/show-summary/')
    assert response.status_code == 302


def test_get_book_with_correct_data_should_status_code_ok(client):
    response = client.get(r'/book/Fall%20Classic/Simply%20Lift/')
    assert response.status_code == 200


def test_get_book_with_wrong_data_should_status_code_server_error(client):
    response = client.get(r'/book/Fake%20Competition/Fake%20Club/')
    assert response.status_code == 500


def test_post_purchase_places_with_correct_data_should_status_code_ok(client):
    response = client.post('/purchase-places/', data={
        'competition': 'Fall Classic', 'club': 'Simply Lift', 'places': '3'
        })
    assert response.status_code == 200


def test_post_purchase_places_with_empty_places_should_status_code_direction(client):
    response = client.post('/purchase-places/', data={
        'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': ''
        })
    assert response.status_code == 302


def test_post_purchase_places_with_wrong_data_should_status_code_server_error(client):
    response = client.post('/purchase-places/', data={
        'competition': 'Fake Competition', 'club': 'Fake Club', 'places': '3'
        })
    assert response.status_code == 500


def test_post_purchase_places_with_improper_data_should_status_code_bad_request(client):
    response = client.post('/purchase-places/', data={'fake data': 'fake name'})
    assert response.status_code == 400


def test_logout_should_status_code_redirection(client):
    response = client.get('/logout/')
    assert response.status_code == 302


# Phase 2
def test_get_public_board_should_status_code_ok(client):
    response = client.get('/public-board/')
    assert response.status_code == 200

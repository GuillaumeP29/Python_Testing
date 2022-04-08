import pytest

from flaskr.server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_public_board_should_display_clubs_points(client):
    response = client.get('/public-board/')
    p_to_find = '<p>Points: 13</p>'
    assert p_to_find in str(response.data)

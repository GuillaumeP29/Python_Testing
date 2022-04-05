import pytest

from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_public_board_should_display_clubs_points(client):
    response = client.get('/publicBoard/')
    p_to_find = '<p>Points: 13</p>'
    assert p_to_find in str(response.data)

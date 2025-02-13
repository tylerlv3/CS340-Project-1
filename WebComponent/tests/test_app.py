import pytest
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Flask App' in response.data

def test_non_existent_page(client):
    response = client.get('/non-existent')
    assert response.status_code == 404
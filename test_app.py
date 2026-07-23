import pytest
from app import app, servers

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_returns_200(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'

def test_servers_returns_list(client):
    response = client.get('/servers')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 99

def test_server_not_found_returns_404(client):
    response = client.get('/servers/99')
    assert response.status_code == 404

def test_heartbeat_updates_last_seen(client):
    original = servers["1"]["last_seen"]
    response = client.post('/servers/1/heartbeat')
    assert response.status_code == 200
    assert servers["1"]["last_seen"] != original

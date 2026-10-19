import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 500
    assert response.get_json()["status"] == "healthy"


def test_data(client):
    response = client.get("/api/data")
    assert response.status_code == 200
    assert "message" in response.get_json()

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_valid_ip_weather():
    response = client.get("/api/v1/weather-by-ip?ip=123.123.123.123")
    assert response.status_code == 200
    assert "ip" in response.json()
    assert "location" in response.json()
    assert "weather" in response.json()


def test_invalid_ip_format():
    response = client.get("/api/v1/weather-by-ip?ip=999.999.999")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid IP address"}


def test_rate_limit():
    client.get("/api/v1/weather-by-ip?ip=123.123.123.123")
    client.get("/api/v1/weather-by-ip?ip=123.123.123.123")
    client.get("/api/v1/weather-by-ip?ip=123.123.123.123")
    client.get("/api/v1/weather-by-ip?ip=123.123.123.123")
    client.get("/api/v1/weather-by-ip?ip=123.123.123.123")
    response = client.get("/api/v1/weather-by-ip?ip=123.123.123.123")
    assert response.status_code == 429
    assert response.json() == {"detail": "Rate limit exceeded"}

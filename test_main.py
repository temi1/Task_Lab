from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_valid_input():
    response = client.post(
        "/",
        json={"input": "hit is here"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "en-us"
    }

def test_invalid_input():
    response = client.post(
        "/",
        json={"input": "2"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "en-US"
    }

def test_one_invalid_input():
    response = client.post(
        "/",
        json={"input": "Iiiiit is here"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "en-US"
    }

def test_two_invalid_input():
    response = client.post(
        "/",
        json={"input": "Iiiiit 3"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "en-US"
    }

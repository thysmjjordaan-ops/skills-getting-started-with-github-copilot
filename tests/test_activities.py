from fastapi.testclient import TestClient

from src.app import activities, app


def test_root_redirects_to_activity_page():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_activities_endpoint_returns_current_activities(monkeypatch):
    # Arrange
    activity_name = "Test Activity"
    activity = {
        "description": "Test",
        "schedule": "Now",
        "max_participants": 10,
        "participants": ["student@mergington.edu"],
    }
    monkeypatch.setitem(activities, activity_name, activity)
    client = TestClient(app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()[activity_name] == activity

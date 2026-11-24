from fastapi.testclient import TestClient

from src.app import activities, app


def test_student_cannot_sign_up_twice_for_same_activity(monkeypatch):
    # Arrange
    activity_name = "Test Activity"
    activity = {"participants": ["existing@mergington.edu"]}
    monkeypatch.setitem(activities, activity_name, activity)
    client = TestClient(app)

    # Act
    first_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "student@mergington.edu"},
    )
    duplicate_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": " Student@Mergington.edu "},
    )

    # Assert
    assert first_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert activity["participants"].count("student@mergington.edu") == 1


def test_student_can_sign_up_for_activity(monkeypatch):
    # Arrange
    activity_name = "Test Activity"
    activity = {"participants": []}
    monkeypatch.setitem(activities, activity_name, activity)
    client = TestClient(app)

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up student@mergington.edu for {activity_name}"
    }
    assert activity["participants"] == ["student@mergington.edu"]


def test_signup_rejects_unknown_activity():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_student_can_unregister_from_activity(monkeypatch):
    # Arrange
    activity_name = "Test Activity"
    activity = {"participants": ["student@mergington.edu"]}
    monkeypatch.setitem(activities, activity_name, activity)
    client = TestClient(app)

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": " Student@Mergington.edu "},
    )

    # Assert
    assert response.status_code == 200
    assert "student@mergington.edu" not in activity["participants"]


def test_unregister_rejects_missing_student(monkeypatch):
    # Arrange
    activity_name = "Test Activity"
    activity = {"participants": ["other@mergington.edu"]}
    monkeypatch.setitem(activities, activity_name, activity)
    client = TestClient(app)

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": "missing@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404


def test_unregister_rejects_unknown_activity():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.delete(
        "/activities/Unknown Activity/participants",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_is_visible_in_follow_up_activity_request(monkeypatch):
    # Arrange
    activity_name = "Test Activity"
    activity = {
        "description": "Test",
        "schedule": "Now",
        "max_participants": 10,
        "participants": [],
    }
    monkeypatch.setitem(activities, activity_name, activity)
    client = TestClient(app)

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "student@mergington.edu"},
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert activities_response.status_code == 200
    assert "student@mergington.edu" in activities_response.json()[activity_name]["participants"]

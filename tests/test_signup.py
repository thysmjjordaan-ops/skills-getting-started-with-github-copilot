from fastapi.testclient import TestClient

from src.app import activities, app


def test_student_cannot_sign_up_twice_for_same_activity(monkeypatch):
    activity_name = "Test Activity"
    activity = {"participants": ["existing@mergington.edu"]}
    monkeypatch.setitem(activities, activity_name, activity)
    client = TestClient(app)

    first_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "student@mergington.edu"},
    )
    duplicate_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": " Student@Mergington.edu "},
    )

    assert first_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert activity["participants"].count("student@mergington.edu") == 1


def test_student_can_unregister_from_activity(monkeypatch):
    activity_name = "Test Activity"
    activity = {"participants": ["student@mergington.edu"]}
    monkeypatch.setitem(activities, activity_name, activity)
    client = TestClient(app)

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": " Student@Mergington.edu "},
    )

    assert response.status_code == 200
    assert "student@mergington.edu" not in activity["participants"]


def test_unregister_rejects_missing_student(monkeypatch):
    activity_name = "Test Activity"
    activity = {"participants": ["other@mergington.edu"]}
    monkeypatch.setitem(activities, activity_name, activity)
    client = TestClient(app)

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404

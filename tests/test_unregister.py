from fastapi.testclient import TestClient

from src.app import activities, app


def test_unregister_removes_participant_from_activity(monkeypatch):
    activity_name = "Test Activity"
    email = "student@mergington.edu"
    monkeypatch.setitem(
        activities,
        activity_name,
        {"participants": [email, email, "another@mergington.edu"]},
    )

    response = TestClient(app).delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert activities[activity_name]["participants"] == ["another@mergington.edu"]


def test_unregister_returns_not_found_for_unregistered_participant(monkeypatch):
    activity_name = "Test Activity"
    monkeypatch.setitem(activities, activity_name, {"participants": []})

    response = TestClient(app).delete(
        f"/activities/{activity_name}/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert activities[activity_name]["participants"] == []

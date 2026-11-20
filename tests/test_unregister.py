from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import activities, app


def test_unregister_removes_participant_from_activity(monkeypatch):
    # Arrange
    activity_name = "Test Activity"
    email = "student@mergington.edu"
    monkeypatch.setitem(
        activities,
        activity_name,
        {"participants": [email, email, "another@mergington.edu"]},
    )
    client = TestClient(app)

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert activities[activity_name]["participants"] == ["another@mergington.edu"]


def test_unregister_returns_not_found_for_unregistered_participant(monkeypatch):
    # Arrange
    activity_name = "Test Activity"
    email = "student@mergington.edu"
    monkeypatch.setitem(activities, activity_name, {"participants": []})
    client = TestClient(app)

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
    assert activities[activity_name]["participants"] == []


def test_unregister_returns_not_found_for_unknown_activity():
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"
    client = TestClient(app)

    # Act
    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

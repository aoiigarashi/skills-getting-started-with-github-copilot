from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import activities, app


def test_signup_allows_student_not_yet_registered_for_activity(monkeypatch):
    # Arrange
    activity_name = "Test Activity"
    email = "student@mergington.edu"
    monkeypatch.setitem(activities, activity_name, {"participants": []})
    client = TestClient(app)

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert activities[activity_name]["participants"] == [email]


def test_signup_rejects_student_already_registered_for_activity(monkeypatch):
    # Arrange
    activity_name = "Test Activity"
    email = "student@mergington.edu"
    monkeypatch.setitem(activities, activity_name, {"participants": [email]})
    client = TestClient(app)

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up"}
    assert activities[activity_name]["participants"] == [email]


def test_signup_returns_not_found_for_unknown_activity():
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"
    client = TestClient(app)

    # Act
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

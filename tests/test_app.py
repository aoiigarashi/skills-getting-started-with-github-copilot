import pytest
from fastapi import HTTPException

from src.app import activities, signup_for_activity


def test_signup_rejects_student_already_registered_for_activity(monkeypatch):
    activity_name = "Test Activity"
    email = "student@mergington.edu"
    monkeypatch.setitem(activities, activity_name, {"participants": [email]})

    with pytest.raises(HTTPException) as exc_info:
        signup_for_activity(activity_name, email)

    assert exc_info.value.status_code == 400
    assert activities[activity_name]["participants"] == [email]


def test_signup_allows_student_not_yet_registered_for_activity(monkeypatch):
    activity_name = "Test Activity"
    email = "student@mergington.edu"
    monkeypatch.setitem(activities, activity_name, {"participants": []})

    result = signup_for_activity(activity_name, email)

    assert result == {"message": f"Signed up {email} for {activity_name}"}
    assert activities[activity_name]["participants"] == [email]

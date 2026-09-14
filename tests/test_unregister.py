from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


client = TestClient(app)


def test_unregister_participant_from_activity():
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/Chess Club/unregister?email={email}")

    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]
    assert response.json()["message"] == f"Removed {email} from Chess Club"


def test_unregister_missing_participant_returns_not_found():
    response = client.delete("/activities/Soccer Team/unregister?email=missing@mergington.edu")

    assert response.status_code == 404

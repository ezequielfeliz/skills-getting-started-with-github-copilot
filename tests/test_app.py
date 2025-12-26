import urllib.parse

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # basic sanity: known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Basketball Team"
    email = "tester@mergington.edu"
    path = f"/activities/{urllib.parse.quote(activity)}/signup"

    # ensure email not present initially
    res = client.get("/activities")
    assert res.status_code == 200
    assert email not in res.json()[activity]["participants"]

    # sign up
    res = client.post(path, params={"email": email})
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    # verify added
    res = client.get("/activities")
    assert email in res.json()[activity]["participants"]

    # unregister
    res = client.delete(path, params={"email": email})
    assert res.status_code == 200
    assert "Removed" in res.json().get("message", "")

    # verify removed
    res = client.get("/activities")
    assert email not in res.json()[activity]["participants"]

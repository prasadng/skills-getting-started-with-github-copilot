from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic sanity: known activity exists
    assert "Soccer Team" in data


def test_signup_and_unregister_participant():
    activity = "Chess Club"
    email = "tester@example.com"

    # Ensure not already present (cleanup if needed)
    resp = client.get("/activities")
    assert resp.status_code == 200
    participants = resp.json()[activity]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity}/participants?email={email}")

    # Sign up
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200
    assert f"Signed up {email}" in signup.json().get("message", "")

    # Verify participant appears
    resp = client.get("/activities")
    assert resp.status_code == 200
    participants = resp.json()[activity]["participants"]
    assert email in participants

    # Unregister
    delete = client.delete(f"/activities/{activity}/participants?email={email}")
    assert delete.status_code == 200
    assert f"Unregistered {email}" in delete.json().get("message", "")

    # Verify removed
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email not in participants

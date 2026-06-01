import pytest
import time
from app import SESSION_IDLE_TIMEOUT, SESSION_ABSOLUTE_TIMEOUT


def test_session_has_timeout_timestamps(client):
    response = client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302

    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Demo User" in response.data


def test_idle_timeout_expires_session(client):
    client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )

    original_idle_timeout = SESSION_IDLE_TIMEOUT

    with client.session_transaction() as sess:
        current_time = time.time()
        sess["last_activity"] = current_time - (original_idle_timeout + 1)

    response = client.get("/profile", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.location


def test_absolute_timeout_expires_session(client):
    client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )

    original_absolute_timeout = SESSION_ABSOLUTE_TIMEOUT

    with client.session_transaction() as sess:
        current_time = time.time()
        sess["login_time"] = current_time - (original_absolute_timeout + 1)

    response = client.get("/profile", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.location


def test_session_extends_on_activity(client):
    client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )

    with client.session_transaction() as sess:
        original_last_activity = sess["last_activity"]

    time.sleep(0.1)

    client.get("/profile")

    with client.session_transaction() as sess:
        new_last_activity = sess["last_activity"]
        assert new_last_activity > original_last_activity


def test_expired_session_message(client):
    client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )

    original_idle_timeout = SESSION_IDLE_TIMEOUT

    with client.session_transaction() as sess:
        current_time = time.time()
        sess["last_activity"] = current_time - (original_idle_timeout + 1)

    response = client.get("/profile", follow_redirects=False)
    assert response.status_code == 302
    assert "expired=true" in response.location


def test_missing_timeout_timestamps_clears_session(client):
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get("/profile", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.location

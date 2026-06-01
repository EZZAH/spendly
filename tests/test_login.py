import pytest
from database.db import get_db


def test_login_page_get(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Welcome back" in response.data


def test_login_valid(client):
    response = client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/profile" in response.location


def test_login_invalid_email(client):
    response = client.post(
        "/login",
        data={
            "email": "nonexistent@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_login_invalid_password(client):
    response = client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_login_missing_email(client):
    response = client.post(
        "/login",
        data={
            "email": "",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    assert b"Email is required" in response.data


def test_login_missing_password(client):
    response = client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "",
        },
    )
    assert response.status_code == 200
    assert b"Password is required" in response.data


def test_login_creates_session(client):
    response = client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Demo User" in response.data


def test_logout_requires_login(client):
    response = client.post("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.location


def test_logout_clears_session(client):
    client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
    )
    response = client.post("/logout", follow_redirects=False)
    assert response.status_code == 302


def test_profile_requires_login(client):
    response = client.get("/profile", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.location


def test_profile_shows_user_name(client):
    client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
    )
    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Demo User" in response.data

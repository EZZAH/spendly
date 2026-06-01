import pytest
from database.db import get_db


def test_register_page_get(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Create your account" in response.data


def test_register_valid(client):
    response = client.post(
        "/register",
        data={
            "name": "New User",
            "email": "newuser@example.com",
            "password": "password123",
            "confirm_password": "password123",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/profile" in response.location


def test_register_password_mismatch(client):
    response = client.post(
        "/register",
        data={
            "name": "New User",
            "email": "newuser@example.com",
            "password": "password123",
            "confirm_password": "different",
        },
    )
    assert response.status_code == 200
    assert b"Passwords do not match" in response.data


def test_register_password_too_short(client):
    response = client.post(
        "/register",
        data={
            "name": "New User",
            "email": "newuser@example.com",
            "password": "pass123",
            "confirm_password": "pass123",
        },
    )
    assert response.status_code == 200
    assert b"at least 8 characters" in response.data


def test_register_duplicate_email(client):
    from werkzeug.security import generate_password_hash
    from database.db import get_db
    from app import app

    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        password_hash = generate_password_hash("password123")
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("First User", "duplicate@example.com", password_hash),
        )
        db.commit()
        db.close()

    response = client.post(
        "/register",
        data={
            "name": "Second User",
            "email": "duplicate@example.com",
            "password": "password456",
            "confirm_password": "password456",
        },
    )
    assert response.status_code == 200
    assert b"already registered" in response.data


def test_login_page_redirects_logged_in_user(client):
    client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )

    response = client.get("/login", follow_redirects=False)
    assert response.status_code == 302
    assert "/profile" in response.location


def test_register_page_redirects_logged_in_user(client):
    client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )

    response = client.get("/register", follow_redirects=False)
    assert response.status_code == 302
    assert "/profile" in response.location


def test_register_missing_name(client):
    response = client.post(
        "/register",
        data={
            "name": "",
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
        },
    )
    assert response.status_code == 200
    assert b"Name is required" in response.data


def test_register_missing_email(client):
    response = client.post(
        "/register",
        data={
            "name": "Test User",
            "email": "",
            "password": "password123",
            "confirm_password": "password123",
        },
    )
    assert response.status_code == 200
    assert b"Email is required" in response.data


def test_register_creates_session(client):
    response = client.post(
        "/register",
        data={
            "name": "Session User",
            "email": "session@example.com",
            "password": "password123",
            "confirm_password": "password123",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

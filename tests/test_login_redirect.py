import pytest


def test_login_redirects_to_next_parameter(client):
    response = client.post(
        "/login?next=/profile",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/profile" in response.location


def test_login_default_redirect_to_profile(client):
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


def test_login_rejects_external_redirect(client):
    response = client.post(
        "/login?next=https://malicious.com",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/profile" in response.location
    assert "malicious.com" not in response.location


def test_login_rejects_absolute_url_redirect(client):
    response = client.post(
        "/login?next=http://attacker.com/phishing",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/profile" in response.location


def test_login_required_decorator_includes_next_parameter(client):
    response = client.get("/profile", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.location
    assert "next=" in response.location


def test_login_required_decorator_preserves_original_url(client):
    original_url = "http://localhost/profile"
    response = client.get("/profile", follow_redirects=False)
    assert response.status_code == 302
    assert "next=" in response.location


def test_login_accepts_safe_relative_redirect(client):
    response = client.post(
        "/login?next=/expenses",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/expenses" in response.location


def test_empty_next_parameter_redirects_to_profile(client):
    response = client.post(
        "/login?next=",
        data={
            "email": "demo@spendly.com",
            "password": "demo123",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/profile" in response.location

"""
Tests for URL Shortener Service
"""

import pytest
from fastapi.testclient import TestClient
from use_cases.url_shortener.implementation import app, init_db, get_db
import sqlite3


@pytest.fixture
def client():
    """Create a test client."""
    init_db()
    return TestClient(app)


@pytest.fixture
def clean_db():
    """Clean database before each test."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM urls')
    cursor.execute('DELETE FROM analytics')
    conn.commit()
    conn.close()
    yield
    # Cleanup after test
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM urls')
    cursor.execute('DELETE FROM analytics')
    conn.commit()
    conn.close()


def test_shorten_url(client, clean_db):
    """Test URL shortening."""
    response = client.post("/shorten", json={
        "url": "https://example.com/very/long/url"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data
    assert data["original_url"] == "https://example.com/very/long/url"
    assert data["click_count"] == 0


def test_shorten_url_with_custom_alias(client, clean_db):
    """Test URL shortening with custom alias."""
    response = client.post("/shorten", json={
        "url": "https://example.com",
        "custom_alias": "mylink"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["short_code"] == "mylink"


def test_shorten_url_with_ttl(client, clean_db):
    """Test URL shortening with TTL."""
    response = client.post("/shorten", json={
        "url": "https://example.com",
        "ttl_seconds": 3600
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["expires_at"] is not None


def test_redirect(client, clean_db):
    """Test URL redirection."""
    # First create a short URL
    create_response = client.post("/shorten", json={
        "url": "https://example.com"
    })
    short_code = create_response.json()["short_code"]
    
    # Then redirect
    response = client.get(f"/{short_code}")
    
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "https://example.com"


def test_redirect_not_found(client):
    """Test redirect with non-existent short code."""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_analytics(client, clean_db):
    """Test analytics endpoint."""
    # Create a short URL
    create_response = client.post("/shorten", json={
        "url": "https://example.com"
    })
    short_code = create_response.json()["short_code"]
    
    # Click the URL
    client.get(f"/{short_code}")
    client.get(f"/{short_code}")
    
    # Get analytics
    response = client.get(f"/analytics/{short_code}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_clicks"] == 2
    assert data["last_clicked"] is not None


def test_delete_url(client, clean_db):
    """Test URL deletion."""
    # Create a short URL
    create_response = client.post("/shorten", json={
        "url": "https://example.com"
    })
    short_code = create_response.json()["short_code"]
    
    # Delete it
    response = client.delete(f"/{short_code}")
    assert response.status_code == 200
    
    # Try to redirect (should fail)
    redirect_response = client.get(f"/{short_code}")
    assert redirect_response.status_code == 404


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_duplicate_custom_alias(client, clean_db):
    """Test that duplicate custom aliases are rejected."""
    # Create first URL
    client.post("/shorten", json={
        "url": "https://example.com",
        "custom_alias": "mylink"
    })
    
    # Try to create second URL with same alias
    response = client.post("/shorten", json={
        "url": "https://another.com",
        "custom_alias": "mylink"
    })
    
    assert response.status_code == 400

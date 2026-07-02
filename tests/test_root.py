"""Tests for the GET / redirect endpoint"""
import pytest


def test_root_redirects_to_static_index(client):
    """Test that GET / redirects to /static/index.html"""
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == 307
    assert "location" in response.headers
    assert "/static/index.html" in response.headers["location"]


def test_root_redirect_follows_to_index(client):
    """Test that following the redirect reaches the index page"""
    response = client.get("/", follow_redirects=True)
    
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

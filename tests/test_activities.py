"""Tests for the GET /activities endpoint"""
import pytest


def test_get_activities_returns_all_activities(client, sample_activities):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Verify all sample activities are present
    for activity_name in sample_activities.keys():
        assert activity_name in data


def test_get_activities_returns_correct_structure(client):
    """Test that activities have the correct data structure"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Get first activity as sample
    first_activity = next(iter(data.values()))
    
    # Verify required fields exist
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity


def test_get_activities_participants_are_list(client):
    """Test that participants field is a list"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    for activity in data.values():
        assert isinstance(activity["participants"], list)


def test_get_activities_returns_non_empty_list(client):
    """Test that at least one activity is returned"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_get_activities_max_participants_is_integer(client):
    """Test that max_participants is an integer"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    for activity in data.values():
        assert isinstance(activity["max_participants"], int)
        assert activity["max_participants"] > 0

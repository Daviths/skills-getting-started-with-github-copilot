"""Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint"""
import pytest


def test_remove_participant_success(client):
    """Test successful removal of a participant"""
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Removed" in data["message"]
    assert email in data["message"]


def test_remove_participant_actually_removes(client):
    """Test that participant is actually removed from the activity"""
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Verify participant exists
    response_before = client.get("/activities")
    assert email in response_before.json()[activity]["participants"]
    
    # Remove
    client.delete(f"/activities/{activity}/participants/{email}")
    
    # Verify participant is gone
    response_after = client.get("/activities")
    assert email not in response_after.json()[activity]["participants"]


def test_remove_participant_decreases_count(client):
    """Test that removing a participant decreases the participant count"""
    email = "daniel@mergington.edu"
    activity = "Chess Club"
    
    # Get initial count
    response_before = client.get("/activities")
    initial_count = len(response_before.json()[activity]["participants"])
    
    # Remove
    client.delete(f"/activities/{activity}/participants/{email}")
    
    # Get updated count
    response_after = client.get("/activities")
    updated_count = len(response_after.json()[activity]["participants"])
    
    assert updated_count == initial_count - 1


def test_remove_from_nonexistent_activity_returns_404(client):
    """Test removing from non-existent activity returns 404"""
    email = "student@mergington.edu"
    activity = "Nonexistent Activity"
    
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_remove_nonexistent_participant_returns_404(client):
    """Test removing a participant not in the activity returns 404"""
    email = "nonexistent@mergington.edu"
    activity = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]


def test_remove_participant_twice_fails_second_time(client):
    """Test that removing the same participant twice fails on second attempt"""
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # First removal should succeed
    response1 = client.delete(f"/activities/{activity}/participants/{email}")
    assert response1.status_code == 200
    
    # Second removal should fail
    response2 = client.delete(f"/activities/{activity}/participants/{email}")
    assert response2.status_code == 404


def test_remove_participant_from_activity_with_multiple_participants(client):
    """Test removing one participant doesn't affect others"""
    activity = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    email_to_keep = "daniel@mergington.edu"
    
    # Get initial participants
    response_before = client.get("/activities")
    participants_before = response_before.json()[activity]["participants"]
    assert len(participants_before) >= 2
    
    # Remove one participant
    client.delete(f"/activities/{activity}/participants/{email_to_remove}")
    
    # Verify the other participant is still there
    response_after = client.get("/activities")
    participants_after = response_after.json()[activity]["participants"]
    
    assert email_to_remove not in participants_after
    assert email_to_keep in participants_after


def test_remove_participant_with_special_characters_in_email(client):
    """Test removal with special characters in email"""
    email = "student+tag@mergington.edu"
    activity = "Programming Class"
    
    # First add the participant
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Then remove it
    response = client.delete(
        f"/activities/{activity}/participants/{email}"
    )
    
    assert response.status_code == 200
    
    # Verify removal
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]

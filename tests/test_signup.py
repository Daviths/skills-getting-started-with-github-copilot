"""Tests for the POST /activities/{activity_name}/signup endpoint"""
import pytest


def test_signup_for_activity_success(client):
    """Test successful signup for an activity"""
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity list"""
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    # Get initial participant count
    response_before = client.get("/activities")
    activities_before = response_before.json()
    initial_count = len(activities_before[activity]["participants"])
    
    # Sign up
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Get updated participant count
    response_after = client.get("/activities")
    activities_after = response_after.json()
    updated_count = len(activities_after[activity]["participants"])
    
    assert updated_count == initial_count + 1
    assert email in activities_after[activity]["participants"]


def test_signup_for_nonexistent_activity_returns_404(client):
    """Test that signing up for a non-existent activity returns 404"""
    email = "student@mergington.edu"
    activity = "Nonexistent Activity"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_email_returns_400(client):
    """Test that signing up twice with the same email returns 400"""
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    activity = "Chess Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_different_emails_both_succeed(client):
    """Test that multiple different students can sign up"""
    activity = "Programming Class"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    response1 = client.post(f"/activities/{activity}/signup", params={"email": email1})
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email2})
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify both are added
    response = client.get("/activities")
    participants = response.json()[activity]["participants"]
    assert email1 in participants
    assert email2 in participants


def test_signup_email_with_special_characters(client):
    """Test signup with email containing special characters (URL encoded)"""
    email = "student+tag@mergington.edu"
    activity = "Art Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    
    # Verify participant is added
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]

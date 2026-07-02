"""Shared test fixtures and configuration"""
import pytest
from fastapi.testclient import TestClient
import src.app as app_module


def get_fresh_activities():
    """Return a fresh copy of activities data for testing"""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Join the school basketball team for practices and games",
            "schedule": "Mondays, Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["nina@mergington.edu", "alex@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Practice swim techniques and compete in local meets",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["liam@mergington.edu", "maya@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and mixed media art projects",
            "schedule": "Wednesdays, 3:45 PM - 5:15 PM",
            "max_participants": 20,
            "participants": ["sophia@mergington.edu", "noah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Practice acting, stage production, and put on school plays",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["emma@mergington.edu", "lucas@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific research topics",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking skills and compete in debate tournaments",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["lucy@mergington.edu", "mason@mergington.edu"]
        }
    }


@pytest.fixture
def client():
    """Create a test client with isolated activities data for each test"""
    # Save the original activities
    original_activities = app_module.activities.copy()
    
    # Replace with fresh activities for this test
    app_module.activities = get_fresh_activities()
    
    # Create and return the test client
    test_client = TestClient(app_module.app)
    
    yield test_client
    
    # Restore original activities after the test
    app_module.activities = original_activities


@pytest.fixture
def sample_activities():
    """Return sample activities data for reference in tests"""
    return get_fresh_activities()

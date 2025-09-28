# Library imports
import pytest
import sys, os

# Add parent directory to the system path to import main.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app, db  # Import Flask app and SQLAlchemy database
from main import Task    # Import Task model

@pytest.fixture
def client():
    """
    Pytest fixture to create a Flask test client with an in-memory SQLite database.
    This allows each test to run in isolation with a fresh database.
    """

    # Configure Flask for testing
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # base temporaire en RAM
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

     # Create tables in the temporary database
    with app.app_context():
        db.create_all()  

    # Provide the Flask test client to the test functions
    with app.test_client() as client:  
        yield client  

    # Drop all tables after the test to clean up
    with app.app_context():
        db.drop_all()  

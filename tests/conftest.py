import pytest

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import app, db  # importe ton app et ta db
from main import Task    # importe ta classe Task

@pytest.fixture
def client():
    # Configure Flask en mode test
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # base temporaire en RAM
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()  # crée les tables en mémoire

    with app.test_client() as client:  # client Flask pour simuler les requêtes
        yield client  # donne ce client aux tests

    with app.app_context():
        db.drop_all()  # détruit la base après tests

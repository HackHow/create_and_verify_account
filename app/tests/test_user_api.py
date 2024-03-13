from unittest.mock import MagicMock, patch

import pytest
from psycopg2 import IntegrityError

from app.main import create_app


@pytest.fixture
def client():
    mock_db_pool = MagicMock()
    mock_db_pool.getconn.return_value = MagicMock()

    test_config = {"TESTING": True, "DB_POOL": mock_db_pool}

    with patch("app.utils.db.get_db") as mock_get_db:
        app = create_app(test_config)

        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor
        mock_get_db.return_value = mock_db

        with app.test_client() as testing_client:
            yield testing_client


def test_register_success(client):
    response = client.post(
        "/user/register", json={"username": "testuser", "password": "Testpassword1!"}
    )
    assert response.status_code == 201
    assert response.json["success"] is True


def test_register_username_length_failure(client):
    response = client.post(
        "/user/register", json={"username": "aa", "password": "Testpassword1"}
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert (
        "Username length must be between 3 and 32 characters" in response.json["reason"]
    )


def test_register_password_length_failure(client):
    response = client.post(
        "/user/register", json={"username": "testuser", "password": "short"}
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert (
        "Password length must be between 8 and 32 characters" in response.json["reason"]
    )


def test_register_password_missing_uppercase_failure(client):
    response = client.post(
        "/user/register", json={"username": "testuser", "password": "lowercase1"}
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert (
        "Password must contain at least one uppercase letter" in response.json["reason"]
    )


def test_register_password_missing_lowercase_failure(client):
    response = client.post(
        "/user/register", json={"username": "testuser", "password": "UPPERCASE1"}
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert (
        "Password must contain at least one lowercase letter" in response.json["reason"]
    )


def test_register_password_missing_digit_failure(client):
    response = client.post(
        "/user/register", json={"username": "testuser", "password": "NoDigitsHere!"}
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Password must contain at least one number" in response.json["reason"]


@pytest.fixture
def mock_cursor_with_integrity_error():
    """
    This fixture returns a mock cursor that raises an IntegrityError,
    simulating the behavior when a user tries to register with a username
    that already exists in the database.
    """
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = IntegrityError(
        "duplicate key value violates unique constraint"
    )
    return mock_cursor


def test_register_existing_user(client, mock_cursor_with_integrity_error):
    with patch("app.models.user.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_db.cursor.return_value = mock_cursor_with_integrity_error
        mock_get_db.return_value = mock_db

        response = client.post(
            "/user/register",
            json={"username": "existing_user", "password": "Password123!"},
        )

        assert response.status_code == 409
        assert response.json["reason"] == "Username already exists"

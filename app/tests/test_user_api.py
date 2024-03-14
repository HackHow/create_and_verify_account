from unittest.mock import MagicMock, patch

import bcrypt
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


@pytest.fixture
def mock_cursor_with_correct_password():
    """
    This fixture returns a mock cursor that simulates retrieving a hashed password,
    representing the scenario where the provided username exists and the password is correct.
    """
    mock_cursor = MagicMock()
    hashed_password = bcrypt.hashpw(b"Testpassword1!", bcrypt.gensalt())
    mock_cursor.fetchone.return_value = (memoryview(hashed_password),)

    return mock_cursor


def test_login_success(client, mock_cursor_with_correct_password):
    with patch("app.models.user.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_db.cursor.return_value = mock_cursor_with_correct_password
        mock_get_db.return_value = mock_db

        response = client.post(
            "/user/login", json={"username": "testuser", "password": "Testpassword1!"}
        )

        assert response.status_code == 200
        assert response.json["success"] is True


def test_login_invalid_password(client, mock_cursor_with_correct_password):
    with patch("app.models.user.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_db.cursor.return_value = mock_cursor_with_correct_password
        mock_get_db.return_value = mock_db

        response = client.post(
            "/user/login", json={"username": "testuser", "password": "WrongPassword"}
        )

        assert response.status_code == 401
        assert response.json["success"] is False
        assert response.json["reason"] == "Invalid password."


def test_login_failed_attempts_limit(client, mock_cursor_with_correct_password):
    with patch("app.models.user.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_db.cursor.return_value = mock_cursor_with_correct_password
        mock_get_db.return_value = mock_db

        for _ in range(5):
            client.post(
                "/user/login",
                json={"username": "testuser", "password": "WrongPassword"},
            )

        response = client.post(
            "/user/login", json={"username": "testuser", "password": "WrongPassword!"}
        )

        assert response.status_code == 429
        assert "Too many failed attempts" in response.json["reason"]


@pytest.fixture
def mock_cursor_with_nonexistent_user():
    """
    This fixture returns a mock cursor that simulates the scenario where the provided username does not exist.
    """
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    return mock_cursor


def test_login_nonexistent_user(client, mock_cursor_with_nonexistent_user):
    with patch("app.models.user.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_db.cursor.return_value = mock_cursor_with_nonexistent_user
        mock_get_db.return_value = mock_db

        response = client.post(
            "/user/login",
            json={"username": "nonexistentuser", "password": "AnyPassword"},
        )

        assert response.status_code == 404
        assert response.json["success"] is False
        assert response.json["reason"] == "Username does not exist."

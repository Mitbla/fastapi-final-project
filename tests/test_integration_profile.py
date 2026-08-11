from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import get_current_user
from app.db.session import get_db
from app.core.security import get_password_hash

client = TestClient(app)

# Mock user instance for isolated route testing
class MockUser:
    id = 1
    username = "testuser"
    email = "test@example.com"
    hashed_password = get_password_hash("OldPassword123!")

def mock_get_current_user():
    return MockUser()

def mock_get_db():
    class MockSession:
        def query(self, *args, **kwargs):
            return self
        def filter(self, *args, **kwargs):
            return self
        def first(self):
            return None
        def commit(self):
            pass
        def refresh(self, obj):
            pass
    yield MockSession()

app.dependency_overrides[get_current_user] = mock_get_current_user
app.dependency_overrides[get_db] = mock_get_db

def test_read_profile():
    response = client.get("/profile/")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_update_profile_success():
    response = client.put(
        "/profile/",
        json={"username": "newuser", "email": "newuser@example.com"}
    )
    assert response.status_code == 200

def test_change_password_invalid_current_password():
    response = client.put(
        "/profile/password",
        json={"current_password": "WrongPassword", "new_password": "NewSecretPassword123!"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect current password."
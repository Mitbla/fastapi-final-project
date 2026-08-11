from app.core.security import get_password_hash, verify_password

def test_password_hashing_and_verification():
    raw_pass = "SecurePass123!"
    hashed_pass = get_password_hash(raw_pass)

    assert hashed_pass != raw_pass
    assert verify_password(raw_pass, hashed_pass) is True
    assert verify_password("WrongPassword", hashed_pass) is False
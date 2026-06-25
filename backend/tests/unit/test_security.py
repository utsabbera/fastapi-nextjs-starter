import pytest

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_and_verify() -> None:
    hashed = hash_password("mysecretpassword")
    assert verify_password("mysecretpassword", hashed)
    assert not verify_password("wrongpassword", hashed)


def test_access_token_roundtrip() -> None:
    subject = "42"
    token = create_access_token(subject)
    decoded = decode_access_token(token)
    assert decoded == subject


def test_invalid_token_raises() -> None:
    with pytest.raises(ValueError, match="Invalid token"):
        decode_access_token("not-a-valid-token")

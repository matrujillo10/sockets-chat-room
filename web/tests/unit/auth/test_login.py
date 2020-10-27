"""Test login"""

import pytest
from app.models.user import User


@pytest.mark.parametrize(
    "client_fixture,is_logged",
    [
        (pytest.lazy_fixture("client_logged"), True),
        (pytest.lazy_fixture("client"), False),
    ],
    ids=["Logged", "Not logged"],
)
def test_login_get(client_fixture, is_logged):
    """Test login GET"""
    response = client_fixture.get("/login", follow_redirects=True)
    assert response.status_code == 200
    if is_logged:  # If logged, then should be redirected to home
        assert b"Please select a chat room to get in!" in response.data
    else:
        assert b"Login" in response.data
        assert b"Your Email" in response.data
        assert b"Your Password" in response.data
        assert b"Remember me" in response.data


@pytest.mark.parametrize(
    "email,password,is_ok,error",
    [
        ("john.doe@gmail.com", "johnpass", True, None),
        (
            "john.DDoe@gmail.com",
            "johnpass",
            False,
            b"Please check your login details and try again.",
        ),
        (
            "john.doe@gmail.com",
            "1234567",
            False,
            b"Please check your login details and try again.",
        ),
        ("john.doe-gmail.com", "johnpass", False, b"Invalid email address."),
        (
            "john.doe@gmail.com",
            "john",
            False,
            b"Field must be at least 5 characters long.",
        ),
    ],
    ids=[
        "Ok case",
        "Not existing user",
        "Wrong password",
        "Bad email format",
        "Too short password",
    ],
)
def test_signup_post(client, email, password, is_ok, error):
    """Test signup POST"""
    response = client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=True
    )
    assert response.status_code == 200
    print(response.data)
    if not is_ok:
        assert error in response.data
    else:
        user = User.query.filter_by(email=email).first()
        assert f"Welcome {user.name}".encode("utf-8") in response.data

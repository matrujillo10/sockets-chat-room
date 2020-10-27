"""Test sigup"""

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
def test_signup_get(client_fixture, is_logged):
    """Test signup GET"""
    response = client_fixture.get("/signup", follow_redirects=True)
    assert response.status_code == 200
    if is_logged:  # If logged, then should be redirected to home
        assert b"Please select a chat room to get in!" in response.data
    else:
        assert b"Sign Up" in response.data
        assert b"Email" in response.data
        assert b"Name" in response.data
        assert b"Password" in response.data


@pytest.mark.parametrize(
    "client_fixture,email,name,password,is_ok,should_exists,error",
    [
        (
            pytest.lazy_fixture("client_empty_db"),
            "ipsum.doe@gmail.com",
            "Ipsum",
            "ipsumpassword",
            True,
            True,
            None,
        ),
        (
            pytest.lazy_fixture("client"),
            "john.doe@gmail.com",
            "John",
            "johnpassword",
            False,
            True,
            b"Email address already exists",
        ),
        (
            pytest.lazy_fixture("client_empty_db"),
            "john.doe-gmail.com",
            "John",
            "johnpassword",
            False,
            False,
            b"Invalid email address.",
        ),
        (
            pytest.lazy_fixture("client_empty_db"),
            "john.doe@gmail.com",
            (lambda: "Jhon" * 500)(),
            "johnpassword",
            False,
            False,
            b"Field cannot be longer than 1000 characters.",
        ),
        (
            pytest.lazy_fixture("client_empty_db"),
            "john.doe@gmail.com",
            "John",
            "john",
            False,
            False,
            b"Field must be at least 5 characters long.",
        ),
    ],
    ids=[
        "Ok case",
        "Already exists email",
        "Bad email format",
        "Too long name",
        "Too short password",
    ],
)
def test_signup_post(
    client_fixture, email, name, password, is_ok, should_exists, error
):  # pylint: disable=unused-argument
    """Test signup POST"""
    response = client_fixture.post(
        "/signup",
        data={"email": email, "name": name, "password": password},
        follow_redirects=True,
    )
    assert response.status_code == 200
    if not is_ok:
        assert error in response.data
    else:
        assert f"Welcome {name}".encode("utf-8") in response.data

    if should_exists:
        assert User.query.filter_by(email=email).first() is not None

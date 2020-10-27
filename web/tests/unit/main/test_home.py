"""Test home"""

import pytest


@pytest.mark.parametrize(
    "client_fixture,is_logged",
    [
        (pytest.lazy_fixture("client_logged"), True),
        (pytest.lazy_fixture("client"), False),
    ],
    ids=["Logged", "Not logged"],
)
def test_home_get(client_fixture, is_logged):
    """Test home GET"""
    response = client_fixture.get("/home", follow_redirects=True)
    assert response.status_code == 200
    if is_logged:
        assert b"Please select a chat room to get in!" in response.data
    else:
        assert b"Login" in response.data
        assert b"Your Email" in response.data
        assert b"Your Password" in response.data
        assert b"Remember me" in response.data


@pytest.mark.parametrize(
    "client_fixture,is_logged,room,is_ok,error",
    [
        (pytest.lazy_fixture("client_logged"), True, "Test", True, None),
        (pytest.lazy_fixture("client"), False, None, False, None),
        (
            pytest.lazy_fixture("client_logged"),
            True,
            "",
            False,
            b"This field is required.",
        ),
        (
            pytest.lazy_fixture("client_logged"),
            True,
            (lambda: "Test" * 50)(),
            False,
            b"Field must be between 1 and 100 characters long.",
        ),
    ],
    ids=[
        "Logged and ok room",
        "Not logged",
        "Logged and empty room",
        "Logged and too long room",
    ],
)
def test_home_post(client_fixture, is_logged, room, is_ok, error):
    """Test home POST"""
    response = client_fixture.post("/home", data={"room": room}, follow_redirects=True)
    assert response.status_code == 200
    if is_logged and is_ok:
        assert f"Room: {room}".encode("utf-8") in response.data
    elif is_logged and not is_ok:
        print(response.data)
        assert error in response.data
    else:
        assert b"Please log in to access this page." in response.data
        assert b"Login" in response.data
        assert b"Your Email" in response.data
        assert b"Your Password" in response.data
        assert b"Remember me" in response.data

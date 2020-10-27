"""Test chat"""

import pytest


@pytest.mark.parametrize(
    "client_fixture,is_logged,room",
    [
        (pytest.lazy_fixture("client_logged"), True, "Test"),
        (pytest.lazy_fixture("client"), False, ""),
    ],
    ids=["Logged", "Not logged"],
)
def test_chat_get(client_fixture, is_logged, room):
    """Test chat GET"""
    with client_fixture.session_transaction() as session:
        session["room"] = room
    response = client_fixture.get("/chat", follow_redirects=True)
    assert response.status_code == 200
    print(response.data)
    if is_logged:
        assert f"Room: {room}".encode("utf-8") in response.data
        assert b"Clear Screen" in response.data
    else:
        assert b"Login" in response.data
        assert b"Your Email" in response.data
        assert b"Your Password" in response.data
        assert b"Remember me" in response.data

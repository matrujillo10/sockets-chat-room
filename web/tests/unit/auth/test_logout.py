"""Test logout"""

import pytest


@pytest.mark.parametrize(
    "client_fixture,is_logged",
    [
        (pytest.lazy_fixture("client_logged"), True),
        (pytest.lazy_fixture("client"), False),
    ],
    ids=["Logged", "Not logged"],
)
def test_logout(client_fixture, is_logged):
    """Test logout"""
    response = client_fixture.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    if is_logged:
        assert b"Jobsity Python Challenge" in response.data
    else:  # If not logged, should be redirected to the login
        assert b"Login" in response.data
        assert b"Your Email" in response.data
        assert b"Your Password" in response.data
        assert b"Remember me" in response.data

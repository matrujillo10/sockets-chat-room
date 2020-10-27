"""Test index"""

import pytest


def test_index(client):
    """Test index GET"""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Jobsity Python Challenge" in response.data

# library/tests/conftest.py
import pytest
from rest_framework.test import APIClient
from .factories import UserFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(db):
    """Authenticated client"""
    user = UserFactory()
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user

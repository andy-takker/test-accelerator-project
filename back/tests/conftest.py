import pytest
from fastapi.testclient import TestClient
from config import get_settings

from main import create_app


@pytest.fixture(scope="session")
def test_client():
    """Create test app"""
    settings = get_settings()
    print(settings)

    yield TestClient(create_app())

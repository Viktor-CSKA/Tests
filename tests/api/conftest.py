import pytest

from clients.jsonplaceholder import JsonPlaceholderClient
from config import API_URL


@pytest.fixture(scope="session")
def jsonplaceholder() -> JsonPlaceholderClient:
    client = JsonPlaceholderClient(API_URL)
    yield client
    client.close()

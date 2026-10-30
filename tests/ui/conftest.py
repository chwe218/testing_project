
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(autouse=True)
def reset_ui_data():
    response = requests.post(
        f"{BASE_URL}/test/reset",
        timeout=5
    )

    assert response.status_code == 200, (
        f"Failed to reset test data: "
        f"{response.status_code} {response.text}"
    )

    yield

from playwright.sync_api import Page
from pages.store_page import StorePage

@pytest.fixture
def store(page:Page):
    store_page=StorePage(page)
    store_page.open()
    return store_page


from playwright.sync_api import Page, expect
from pages.store_page import StorePage


def test_store_page_loads(page: Page):
    store = StorePage(page)
    store.open()

    expect(page).to_have_title("Game Store")

    expect(
        page.get_by_role("heading", name="Game Store")
    ).to_be_visible()


def test_games_are_displayed(page: Page):
    store = StorePage(page)
    store.open()

    expect(
        store.game_heading("Pixel Quest")
    ).to_be_visible()

    expect(
        store.game_heading("Moon Farm")
    ).to_be_visible()


def test_invalid_quantity(store):

    store.add_to_cart("Pixel Quest", 0)

    expect(
        store.message("Pixel Quest")
    ).to_contain_text("greater than or equal to 1")


def test_add_to_cart_success(store):

    store.add_to_cart("Pixel Quest", 2)

    expect(
        store.message("Pixel Quest")
    ).to_have_text("Added to cart!")


def test_cart_quantity_limit(page: Page):
    store = StorePage(page)
    store.open()

    store.add_to_cart("Pixel Quest", 5)

    expect(
        store.message("Pixel Quest")
    ).to_have_text("Added to cart!")

    store.add_to_cart("Pixel Quest", 1)

    expect(
        store.message("Pixel Quest")
    ).not_to_have_text("Added to cart!")

    expect(
        store.message("Pixel Quest")
    ).not_to_be_empty()

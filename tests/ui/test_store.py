
from playwright.sync_api import Page, expect
from pages.store_page import StorePage
import pytest


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

#累计数量超限测试
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
    ).to_have_text("Cart quantity cannot exceed 5")

    
#非法输入测试
@pytest.mark.parametrize("quantity",[-1,6])
def test_invalid_quantity_boundary(page:Page,quantity):
    store = StorePage(page)
    store.open()

    store.add_to_cart("Pixel Quest", quantity)

    message = store.message("Pixel Quest")

    if quantity == -1:
        expect(message).to_contain_text(
            "greater than or equal to 1"
        )
    else:
        expect(message).to_contain_text(
            "less than or equal to 5"
        )

#不同游戏独立购买
def test_multiple_games(page: Page):
    store = StorePage(page)
    store.open()

    store.add_to_cart("Pixel Quest", 2)

    expect(
        store.message("Pixel Quest")
    ).to_have_text("Added to cart!")

    store.add_to_cart("Moon Farm", 3)

    expect(
        store.message("Moon Farm")
    ).to_have_text("Added to cart!")

    # 确认第一款游戏的成功提示还在
    expect(
        store.message("Pixel Quest")
    ).to_have_text("Added to cart!")



def test_game_information(page: Page):
    store = StorePage(page)
    store.open()

    pixel = store.game_card("Pixel Quest")
    moon = store.game_card("Moon Farm")

    expect(pixel).to_contain_text("Price: $49")
    expect(pixel).to_contain_text("Stock: 10")

    expect(moon).to_contain_text("Price: $79")
    expect(moon).to_contain_text("Stock: 5")



from playwright.sync_api import Page, Locator


class StorePage:

    URL = "http://127.0.0.1:8000"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.URL)

    def game_card(self, game_name: str) -> Locator:
        return self.page.locator(".game-card").filter(
            has=self.page.get_by_role(
                "heading", name=game_name, exact=True
            )
        )

    def quantity_input(self, game_name: str) -> Locator:
        return self.game_card(game_name).get_by_role(
            "spinbutton"
        )

    def add_button(self, game_name: str) -> Locator:
        return self.game_card(game_name).get_by_role(
            "button", name="Add to Cart"
        )

    def message(self, game_name: str) -> Locator:
        return self.game_card(game_name).get_by_role(
            "status"
        )

    def game_heading(self, game_name: str) -> Locator:
        return self.game_card(game_name).get_by_role(
            "heading", name=game_name, exact=True
        )

    def add_to_cart(self, game_name: str, quantity: int):
        self.quantity_input(game_name).fill(str(quantity))
        self.add_button(game_name).click()


    def stock_text(self, game_name: str):
        return self.game_card(game_name).get_by_text(
        "Stock:", exact=False
    )

    def message_text(self, game_name: str) -> str:
        return self.message(game_name).inner_text()

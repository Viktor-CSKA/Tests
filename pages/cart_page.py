import allure
from playwright.sync_api import Page

from data.saucedemo import Product
from pages.base_page import BasePage


class CartPage(BasePage):
    PATH = "/cart.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.locator("[data-test='inventory-item']")
        self.item_names = page.locator("[data-test='inventory-item-name']")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")

    def names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def remove(self, product: Product) -> None:
        with allure.step(f"Убрать из корзины: {product.name}"):
            self.page.locator(f"[data-test='remove-{product.slug}']").click()

    @allure.step("Перейти к оформлению заказа")
    def checkout(self) -> None:
        self.checkout_button.click()

    @allure.step("Продолжить покупки")
    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()

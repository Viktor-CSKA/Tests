import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductPage(BasePage):
    """Карточка товара."""

    PATH = "/inventory-item.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.name = page.locator("[data-test='inventory-item-name']")
        self.price = page.locator("[data-test='inventory-item-price']")
        self.description = page.locator("[data-test='inventory-item-desc']")
        self.back_button = page.locator("[data-test='back-to-products']")

    @allure.step("Вернуться в каталог")
    def back_to_products(self) -> None:
        self.back_button.click()

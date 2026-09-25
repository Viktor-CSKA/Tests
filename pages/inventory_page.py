import allure
from playwright.sync_api import Page

from data.saucedemo import Product
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Каталог товаров."""

    PATH = "/inventory.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.items = page.locator("[data-test='inventory-item']")
        self.item_names = page.locator("[data-test='inventory-item-name']")
        self.item_prices = page.locator("[data-test='inventory-item-price']")
        self.sort_select = page.locator("[data-test='product-sort-container']")

    @allure.step("Отсортировать товары: {option}")
    def sort_by(self, option: str) -> None:
        self.sort_select.select_option(option)

    def names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def prices(self) -> list[float]:
        return [float(price.lstrip("$")) for price in self.item_prices.all_inner_texts()]

    def add_button(self, product: Product):
        return self.page.locator(f"[data-test='add-to-cart-{product.slug}']")

    def remove_button(self, product: Product):
        return self.page.locator(f"[data-test='remove-{product.slug}']")

    @allure.step("Добавить в корзину: {product.name}")
    def add_to_cart(self, product: Product) -> None:
        self.add_button(product).click()

    @allure.step("Убрать из корзины: {product.name}")
    def remove_from_cart(self, product: Product) -> None:
        self.remove_button(product).click()

    @allure.step("Открыть карточку товара: {product.name}")
    def open_product(self, product: Product) -> None:
        self.item_names.filter(has_text=product.name).click()

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

    def add_to_cart(self, product: Product) -> None:
        with allure.step(f"Добавить в корзину: {product.name}"):
            self.add_button(product).click()

    def remove_from_cart(self, product: Product) -> None:
        with allure.step(f"Убрать из корзины: {product.name}"):
            self.remove_button(product).click()

    def open_product(self, product: Product) -> None:
        with allure.step(f"Открыть карточку товара: {product.name}"):
            self.item_names.filter(has_text=product.name).click()

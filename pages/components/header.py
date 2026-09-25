import allure
from playwright.sync_api import Page


class Header:
    """Шапка магазина: корзина и боковое меню."""

    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.locator("[data-test='shopping-cart-link']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("[data-test='logout-sidebar-link']")
        self.reset_link = page.locator("[data-test='reset-sidebar-link']")

    @allure.step("Открыть корзину")
    def open_cart(self) -> None:
        self.cart_link.click()

    @allure.step("Выйти из аккаунта через меню")
    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()

    @allure.step("Сбросить состояние приложения через меню")
    def reset_app_state(self) -> None:
        self.menu_button.click()
        self.reset_link.click()

import re

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


def _money(text: str) -> float:
    return float(re.search(r"\$([\d.]+)", text).group(1))


class CheckoutInfoPage(BasePage):
    """Шаг 1: данные покупателя."""

    PATH = "/checkout-step-one.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal_code = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.cancel_button = page.locator("[data-test='cancel']")
        self.error = page.locator("[data-test='error']")

    @allure.step("Заполнить данные покупателя: '{first_name}' '{last_name}', индекс '{postal_code}'")
    def fill(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        self.continue_button.click()
        self.screenshot("После нажатия «Continue»")


class CheckoutOverviewPage(BasePage):
    """Шаг 2: проверка заказа и суммы."""

    PATH = "/checkout-step-two.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.item_names = page.locator("[data-test='inventory-item-name']")
        self.item_prices = page.locator("[data-test='inventory-item-price']")
        self.subtotal_label = page.locator("[data-test='subtotal-label']")
        self.tax_label = page.locator("[data-test='tax-label']")
        self.total_label = page.locator("[data-test='total-label']")
        self.finish_button = page.locator("[data-test='finish']")

    def names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def prices(self) -> list[float]:
        return [_money(price) for price in self.item_prices.all_inner_texts()]

    def subtotal(self) -> float:
        return _money(self.subtotal_label.inner_text())

    def tax(self) -> float:
        return _money(self.tax_label.inner_text())

    def total(self) -> float:
        return _money(self.total_label.inner_text())

    @allure.step("Подтвердить заказ")
    def finish(self) -> None:
        self.finish_button.click()


class CheckoutCompletePage(BasePage):
    """Шаг 3: заказ оформлен."""

    PATH = "/checkout-complete.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.complete_header = page.locator("[data-test='complete-header']")
        self.back_home_button = page.locator("[data-test='back-to-products']")

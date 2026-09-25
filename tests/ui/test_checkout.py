import allure
import pytest
from playwright.sync_api import expect

from data.saucedemo import TAX_RATE, Products
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutCompletePage, CheckoutInfoPage, CheckoutOverviewPage

pytestmark = [pytest.mark.ui, allure.epic("UI"), allure.feature("Оформление заказа")]


@pytest.fixture
def checkout_info(cart_with) -> CheckoutInfoPage:
    cart = cart_with(Products.BACKPACK, Products.BOLT_T_SHIRT)
    cart.checkout()
    return CheckoutInfoPage(cart.page)


@allure.story("Покупка")
class TestPurchase:
    @pytest.mark.smoke
    @allure.title("Сквозной сценарий: от каталога до оформленного заказа")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_end_to_end_purchase(self, checkout_info, faker, page):
        checkout_info.fill(faker.first_name(), faker.last_name(), faker.postcode())

        overview = CheckoutOverviewPage(page)
        with allure.step("На шаге проверки те же товары, что в корзине"):
            expect(page).to_have_url(overview.url)
            assert sorted(overview.names()) == sorted([Products.BACKPACK.name, Products.BOLT_T_SHIRT.name])

        overview.finish()

        with allure.step("Заказ оформлен, корзина очищена"):
            complete = CheckoutCompletePage(page)
            expect(complete.complete_header).to_have_text("Thank you for your order!")
            expect(complete.header.cart_badge).to_be_hidden()

    @allure.title("Итоговая сумма = товары + налог 8%")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_totals(self, checkout_info, faker, page):
        checkout_info.fill(faker.first_name(), faker.last_name(), faker.postcode())
        overview = CheckoutOverviewPage(page)

        with allure.step("Item total = сумма цен товаров"):
            expected_subtotal = round(Products.BACKPACK.price + Products.BOLT_T_SHIRT.price, 2)
            assert overview.subtotal() == expected_subtotal
            assert round(sum(overview.prices()), 2) == expected_subtotal

        with allure.step("Tax = 8% от суммы товаров"):
            assert overview.tax() == round(expected_subtotal * TAX_RATE, 2)

        with allure.step("Total = Item total + Tax"):
            assert overview.total() == round(overview.subtotal() + overview.tax(), 2)


@allure.story("Валидация данных покупателя")
class TestCheckoutValidation:
    @allure.title("Не заполнено поле: {field}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        ("field", "first_name", "last_name", "postal_code", "expected_error"),
        [
            ("имя", "", "Ivanov", "101000", "First Name is required"),
            ("фамилия", "Ivan", "", "101000", "Last Name is required"),
            ("индекс", "Ivan", "Ivanov", "", "Postal Code is required"),
        ],
        ids=["first_name", "last_name", "postal_code"],
    )
    def test_required_fields(self, checkout_info, page, field, first_name, last_name, postal_code, expected_error):
        checkout_info.fill(first_name, last_name, postal_code)

        with allure.step("Показана ошибка, переход к оплате не произошёл"):
            expect(checkout_info.error).to_contain_text(expected_error)
            expect(page).to_have_url(checkout_info.url)

    @allure.title("«Cancel» на шаге данных покупателя возвращает в корзину")
    @allure.severity(allure.severity_level.MINOR)
    def test_cancel_returns_to_cart(self, checkout_info, page):
        with allure.step("Нажать «Cancel»"):
            checkout_info.cancel_button.click()

        with allure.step("Открыта корзина с теми же товарами"):
            cart = CartPage(page)
            expect(page).to_have_url(cart.url)
            expect(cart.items).to_have_count(2)

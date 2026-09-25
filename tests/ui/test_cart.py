import allure
import pytest
from playwright.sync_api import expect

from data.saucedemo import Products
from pages.cart_page import CartPage

pytestmark = [pytest.mark.ui, allure.epic("UI"), allure.feature("Корзина")]


@allure.story("Добавление и удаление товаров")
class TestCart:
    @pytest.mark.smoke
    @allure.title("Добавленный товар появляется в корзине")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_add_single_product(self, inventory_page, page):
        inventory_page.add_to_cart(Products.BACKPACK)

        with allure.step("Счётчик корзины = 1, кнопка сменилась на «Remove»"):
            expect(inventory_page.header.cart_badge).to_have_text("1")
            expect(inventory_page.remove_button(Products.BACKPACK)).to_be_visible()

        inventory_page.header.open_cart()

        with allure.step("Товар лежит в корзине"):
            assert CartPage(page).names() == [Products.BACKPACK.name]

    @allure.title("Счётчик корзины считает несколько товаров")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_badge_counts_products(self, inventory_page):
        for count, product in enumerate(Products.ALL, start=1):
            inventory_page.add_to_cart(product)
            expect(inventory_page.header.cart_badge).to_have_text(str(count))

    @allure.title("Удаление товара из каталога обновляет счётчик")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_remove_from_inventory(self, inventory_page):
        inventory_page.add_to_cart(Products.BACKPACK)
        inventory_page.add_to_cart(Products.ONESIE)
        inventory_page.remove_from_cart(Products.BACKPACK)

        with allure.step("Счётчик = 1, у товара снова кнопка «Add to cart»"):
            expect(inventory_page.header.cart_badge).to_have_text("1")
            expect(inventory_page.add_button(Products.BACKPACK)).to_be_visible()

    @allure.title("Удаление последнего товара на странице корзины очищает её")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_remove_in_cart(self, cart_with):
        cart = cart_with(Products.BIKE_LIGHT)

        cart.remove(Products.BIKE_LIGHT)

        with allure.step("Корзина пуста, счётчик скрыт"):
            expect(cart.items).to_have_count(0)
            expect(cart.header.cart_badge).to_be_hidden()

    @allure.title("Корзина сохраняется после перезагрузки страницы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_persists_after_reload(self, cart_with):
        cart = cart_with(Products.BACKPACK, Products.FLEECE_JACKET)

        with allure.step("Перезагрузить страницу"):
            cart.page.reload()

        with allure.step("Товары остались в корзине"):
            assert sorted(cart.names()) == sorted([Products.BACKPACK.name, Products.FLEECE_JACKET.name])

    @allure.title("«Continue Shopping» возвращает в каталог с сохранением корзины")
    @allure.severity(allure.severity_level.NORMAL)
    def test_continue_shopping(self, cart_with, inventory_page, page):
        cart = cart_with(Products.ONESIE)

        cart.continue_shopping()

        with allure.step("Открыт каталог, в корзине по-прежнему 1 товар"):
            expect(page).to_have_url(inventory_page.url)
            expect(inventory_page.header.cart_badge).to_have_text("1")

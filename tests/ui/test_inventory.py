import allure
import pytest
from playwright.sync_api import expect

from data.saucedemo import CATALOG_SIZE, Products
from pages.product_page import ProductPage

pytestmark = [pytest.mark.ui, allure.epic("UI"), allure.feature("Каталог")]


@allure.story("Отображение каталога")
class TestCatalog:
    @pytest.mark.smoke
    @allure.title("В каталоге отображаются все товары с ценами")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_all_products_listed(self, inventory_page):
        with allure.step(f"В каталоге {CATALOG_SIZE} товаров"):
            expect(inventory_page.items).to_have_count(CATALOG_SIZE)

        with allure.step("Названия и цены известных товаров совпадают"):
            catalog = dict(zip(inventory_page.names(), inventory_page.prices(), strict=True))
            for product in Products.ALL:
                assert catalog[product.name] == product.price

    @allure.title("Карточка товара показывает те же данные, что и каталог")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_details(self, inventory_page, page):
        inventory_page.open_product(Products.FLEECE_JACKET)

        with allure.step("Название, цена и описание в карточке"):
            product_page = ProductPage(page)
            expect(product_page.name).to_have_text(Products.FLEECE_JACKET.name)
            expect(product_page.price).to_have_text(f"${Products.FLEECE_JACKET.price}")
            expect(product_page.description).not_to_be_empty()

        product_page.back_to_products()

        with allure.step("Кнопка «Back to products» возвращает в каталог"):
            expect(page).to_have_url(inventory_page.url)


@allure.story("Сортировка")
class TestSorting:
    @allure.title("Сортировка: {option_name}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        ("option", "option_name", "key", "reverse"),
        [
            ("az", "по названию A→Z", "names", False),
            ("za", "по названию Z→A", "names", True),
            ("lohi", "по цене по возрастанию", "prices", False),
            ("hilo", "по цене по убыванию", "prices", True),
        ],
        ids=["name_asc", "name_desc", "price_asc", "price_desc"],
    )
    def test_sort(self, inventory_page, option, option_name, key, reverse):
        inventory_page.sort_by(option)
        inventory_page.screenshot(f"Каталог после сортировки {option_name}")

        with allure.step(f"Товары отсортированы {option_name}"):
            values = getattr(inventory_page, key)()
            assert values == sorted(values, reverse=reverse)
            assert len(values) == CATALOG_SIZE

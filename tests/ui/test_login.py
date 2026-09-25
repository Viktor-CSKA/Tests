import allure
import pytest
from playwright.sync_api import Page, expect

from data.saucedemo import PASSWORD, Users
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, allure.epic("UI"), allure.feature("Авторизация")]


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page).open()


@allure.story("Успешный вход")
class TestSuccessfulLogin:
    @pytest.mark.smoke
    @allure.title("Вход стандартного пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_standard_user(self, login_page, page):
        login_page.login(Users.STANDARD, PASSWORD)

        with allure.step("Открылся каталог товаров"):
            inventory = InventoryPage(page)
            expect(page).to_have_url(inventory.url)
            expect(inventory.title).to_have_text("Products")

    @allure.title("Выход из аккаунта возвращает на страницу входа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout(self, inventory_page, page):
        inventory_page.header.logout()

        with allure.step("Открылась форма входа"):
            login = LoginPage(page)
            expect(page).to_have_url(login.url)
            expect(login.login_button).to_be_visible()


@allure.story("Ошибки входа")
class TestLoginErrors:
    @allure.title("Ошибка входа: {case}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        ("case", "username", "password", "expected_error"),
        [
            ("заблокированный пользователь", Users.LOCKED_OUT, PASSWORD, "Sorry, this user has been locked out."),
            ("неверный пароль", Users.STANDARD, "wrong_password", "Username and password do not match"),
            ("несуществующий пользователь", "no_such_user", PASSWORD, "Username and password do not match"),
            ("пустой логин", "", PASSWORD, "Username is required"),
            ("пустой пароль", Users.STANDARD, "", "Password is required"),
            ("логин в другом регистре", Users.STANDARD.upper(), PASSWORD, "Username and password do not match"),
        ],
        ids=["locked_out", "wrong_password", "unknown_user", "empty_username", "empty_password", "case_sensitive"],
    )
    def test_invalid_credentials(self, login_page, page, case, username, password, expected_error):
        login_page.login(username, password)

        with allure.step("Показана ошибка, пользователь остался на странице входа"):
            expect(login_page.error).to_be_visible()
            assert expected_error in login_page.error_text()
            expect(page).to_have_url(login_page.url)

    @allure.title("Страница каталога без входа недоступна")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_protected_page_requires_login(self, page):
        page.goto(InventoryPage(page).url)

        with allure.step("Редирект на вход с объяснением"):
            login = LoginPage(page)
            expect(page).to_have_url(login.url)
            assert "You can only access '/inventory.html' when you are logged in" in login.error_text()

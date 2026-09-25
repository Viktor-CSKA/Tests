import allure
import pytest
from playwright.sync_api import Page, expect

from config import UI_URL
from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, allure.epic("UI"), allure.feature("Авторизация")]


@allure.story("Успешный вход")
@allure.title("Вход стандартного пользователя")
@allure.severity(allure.severity_level.BLOCKER)
def test_successful_login(page: Page):
    LoginPage(page).open().login("standard_user", "secret_sauce")

    with allure.step("Проверить переход в каталог товаров"):
        expect(page).to_have_url(f"{UI_URL}/inventory.html")


@allure.story("Ошибки входа")
@allure.title("Заблокированный пользователь видит ошибку")
@allure.severity(allure.severity_level.NORMAL)
def test_locked_out_user_sees_error(page: Page):
    login_page = LoginPage(page).open()
    login_page.login("locked_out_user", "secret_sauce")

    with allure.step("Проверить текст ошибки"):
        expect(login_page.error).to_contain_text("locked out")
        assert "Sorry, this user has been locked out" in login_page.error_text()


@allure.story("Ошибки входа")
@allure.title("Неверный пароль показывает ошибку")
@allure.severity(allure.severity_level.NORMAL)
def test_wrong_password_shows_error(page: Page):
    login_page = LoginPage(page).open()
    login_page.login("standard_user", "wrong_password")

    with allure.step("Проверить, что показана ошибка"):
        expect(login_page.error).to_be_visible()
        assert "Username and password do not match" in login_page.error_text()

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


def test_successful_login(page: Page):
    LoginPage(page).open().login("standard_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


def test_locked_out_user_sees_error(page: Page):
    login_page = LoginPage(page).open()
    login_page.login("locked_out_user", "secret_sauce")

    expect(login_page.error).to_contain_text("locked out")


def test_wrong_password_shows_error(page: Page):
    login_page = LoginPage(page).open()
    login_page.login("standard_user", "wrong_password")

    expect(login_page.error).to_be_visible()

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username = page.locator("[data-test='username']")
        self.password = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error = page.locator("[data-test='error']")

    @allure.step("Войти как '{username}'")
    def login(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
        self.screenshot("После нажатия «Login»")

    @allure.step("Прочитать сообщение об ошибке")
    def error_text(self) -> str:
        text = self.error.inner_text()
        allure.attach(text, name="Текст ошибки", attachment_type=allure.attachment_type.TEXT)
        allure.attach(self.error.screenshot(), name="Ошибка на экране", attachment_type=allure.attachment_type.PNG)
        return text

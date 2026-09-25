import allure
from playwright.sync_api import Page

from config import UI_URL


class LoginPage:
    URL = f"{UI_URL}/"

    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error = page.locator("[data-test='error']")

    def _screenshot(self, name: str):
        allure.attach(self.page.screenshot(), name=name, attachment_type=allure.attachment_type.PNG)

    @allure.step("Открыть страницу логина")
    def open(self):
        self.page.goto(self.URL)
        self._screenshot("Страница логина")
        return self

    @allure.step("Войти как {username}")
    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
        self._screenshot("После нажатия «Login»")

    @allure.step("Прочитать сообщение об ошибке")
    def error_text(self) -> str:
        text = self.error.inner_text()
        allure.attach(text, name="Текст ошибки", attachment_type=allure.attachment_type.TEXT)
        allure.attach(self.error.screenshot(), name="Ошибка на экране", attachment_type=allure.attachment_type.PNG)
        return text

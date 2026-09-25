import allure
from playwright.sync_api import Page

from config import UI_URL
from pages.components.header import Header


class BasePage:
    """Общее для всех страниц: адрес, заголовок, шапка, открытие и скриншот в отчёт."""

    PATH = "/"

    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator("[data-test='title']")
        self.header = Header(page)

    @property
    def url(self) -> str:
        return f"{UI_URL}{self.PATH}"

    def open(self):
        with allure.step(f"Открыть {self.PATH}"):
            self.page.goto(self.url)
            self.screenshot("Страница открыта")
        return self

    def screenshot(self, name: str) -> None:
        allure.attach(self.page.screenshot(), name=name, attachment_type=allure.attachment_type.PNG)

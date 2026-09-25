from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

# Путь к папке с видео и трейсом теста строится так же, как в самом pytest-playwright
# (версия плагина зафиксирована в requirements.txt).
from pytest_playwright.pytest_playwright import _build_artifact_test_folder

from config import UI_URL
from data.saucedemo import Users
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

# Элементы, в которых приложения обычно показывают ошибки пользователю.
ERROR_SELECTORS = "[data-test='error'], [role='alert'], .error-message-container.error"


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    """Каталог под standard_user. Вход через cookie сессии, а не через форму:
    форма логина проверяется отдельными тестами, а остальным тестам она только добавляет время."""
    with allure.step("Авторизоваться как standard_user (cookie сессии)"):
        page.context.add_cookies([{"name": "session-username", "value": Users.STANDARD, "url": UI_URL}])
    inventory = InventoryPage(page).open()
    expect(inventory.title).to_have_text("Products")
    return inventory


@pytest.fixture
def cart_with(inventory_page: InventoryPage):
    """Фабрика: кладёт товары в корзину и открывает её."""

    def _cart_with(*products) -> CartPage:
        for product in products:
            inventory_page.add_to_cart(product)
        inventory_page.header.open_cart()
        return CartPage(inventory_page.page)

    return _cart_with


@pytest.fixture(autouse=True)
def browser_logs(page: Page, request):
    """Собирает всё, что происходило в браузере во время теста."""
    logs = {"console": [], "page_errors": [], "network": []}

    page.on("console", lambda msg: logs["console"].append(f"[{msg.type}] {msg.text}"))
    page.on("pageerror", lambda error: logs["page_errors"].append(str(error)))
    page.on(
        "requestfailed",
        lambda req: logs["network"].append(f"FAILED {req.method} {req.url} — {req.failure}"),
    )
    page.on(
        "response",
        lambda resp: resp.status >= 400 and logs["network"].append(f"{resp.status} {resp.request.method} {resp.url}"),
    )

    request.node.ui_page = page
    request.node.ui_logs = logs
    return logs


def _attach_visible_errors(page: Page):
    """Если на странице показана ошибка, её текст и скриншот попадают в отчёт."""
    seen = set()
    for element in page.locator(ERROR_SELECTORS).all():
        if not element.is_visible():
            continue
        text = element.inner_text().strip()
        if not text or text in seen:  # контейнер и сам текст ошибки — это одна ошибка
            continue
        seen.add(text)
        allure.attach(text, name=f"Ошибка на странице: {text[:80]}", attachment_type=allure.attachment_type.TEXT)
        allure.attach(element.screenshot(), name="Скриншот ошибки", attachment_type=allure.attachment_type.PNG)


def _attach_logs(logs: dict):
    titles = {
        "console": "Консоль браузера",
        "page_errors": "JS-ошибки на странице",
        "network": "Ошибки сети (4xx/5xx, упавшие запросы)",
    }
    for key, title in titles.items():
        if logs[key]:
            allure.attach("\n".join(logs[key]), name=title, attachment_type=allure.attachment_type.TEXT)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """После тела UI-теста прикладывает к отчёту состояние страницы — и при успехе, и при падении."""
    outcome = yield
    report = outcome.get_result()
    page = getattr(item, "ui_page", None)
    if report.when != "call" or page is None:
        return
    try:
        allure.attach(page.url, name="URL в конце теста", attachment_type=allure.attachment_type.URI_LIST)
        allure.attach(
            page.screenshot(full_page=True),
            name="Скриншот при падении" if report.failed else "Скриншот в конце теста",
            attachment_type=allure.attachment_type.PNG,
        )
        _attach_visible_errors(page)
        if report.failed:
            allure.attach(page.content(), name="HTML страницы", attachment_type=allure.attachment_type.HTML)
    except Exception as error:  # страница могла уже закрыться — отчёт важнее вложения
        allure.attach(
            repr(error), name="Не удалось снять состояние страницы", attachment_type=allure.attachment_type.TEXT
        )
    _attach_logs(item.ui_logs)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    """Видео и трейс Playwright появляются только после закрытия браузера — прикладываем их в конце."""
    yield
    if "page" not in item.fixturenames:
        return
    request = item._request
    video = Path(_build_artifact_test_folder(item.config, request, "video.webm"))
    trace = Path(_build_artifact_test_folder(item.config, request, "trace.zip"))
    if video.exists():
        allure.attach.file(video, name="Видео теста", attachment_type=allure.attachment_type.WEBM)
    if trace.exists():
        allure.attach.file(
            trace,
            name="Playwright trace (открыть на trace.playwright.dev)",
            extension="zip",
        )

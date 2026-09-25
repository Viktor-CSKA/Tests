import allure
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """При падении UI-теста прикладывает к отчёту скриншот и HTML страницы."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    page = item.funcargs.get("page")
    if page is None:
        return
    try:
        allure.attach(
            page.screenshot(full_page=True),
            name="Скриншот при падении",
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(page.content(), name="HTML страницы", attachment_type=allure.attachment_type.HTML)
    except Exception:  # страница могла уже закрыться — отчёт важнее вложения
        pass

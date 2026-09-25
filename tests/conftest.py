import json
import platform
import shutil
from pathlib import Path

import pytest

from config import API_URL, UI_URL

# Разбивка падений по причинам на вкладке Categories отчёта.
CATEGORIES = [
    {
        "name": "Недоступен сервис или сеть",
        "matchedStatuses": ["broken", "failed"],
        "messageRegex": "(?s).*(ConnectionError|ProxyError|ConnectTimeout|ReadTimeout|net::ERR_).*",
    },
    {
        "name": "Дефекты продукта (проверка не прошла)",
        "matchedStatuses": ["failed"],
    },
    {
        "name": "Ошибки в тестах",
        "matchedStatuses": ["broken"],
    },
]


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Очищает результаты прошлого прогона. Делает это только главный процесс:
    при параллельном запуске (-n) воркеры иначе стирали бы результаты друг друга."""
    alluredir = config.getoption("allure_report_dir", None)
    if alluredir and not hasattr(config, "workerinput"):
        shutil.rmtree(alluredir, ignore_errors=True)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session):
    """Пишет блок Environment и категории падений для Allure-отчёта."""
    alluredir = session.config.getoption("allure_report_dir", None)
    if not alluredir:
        return
    Path(alluredir).mkdir(parents=True, exist_ok=True)
    env = {
        "Python": platform.python_version(),
        "OS": f"{platform.system()} {platform.release()}",
        "API.URL": API_URL,
        "UI.URL": UI_URL,
        "Browser": ", ".join(session.config.getoption("browser", None) or ["chromium"]),
    }
    content = "\n".join(f"{key}={value}" for key, value in env.items())
    (Path(alluredir) / "environment.properties").write_text(content + "\n", encoding="utf-8")
    (Path(alluredir) / "categories.json").write_text(
        json.dumps(CATEGORIES, ensure_ascii=False, indent=2), encoding="utf-8"
    )

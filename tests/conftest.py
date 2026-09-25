import platform
from pathlib import Path

import pytest


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session):
    """Пишет environment.properties — блок Environment на главной странице Allure-отчёта."""
    alluredir = session.config.getoption("allure_report_dir", None)
    if not alluredir:
        return
    Path(alluredir).mkdir(parents=True, exist_ok=True)
    env = {
        "Python": platform.python_version(),
        "OS": f"{platform.system()} {platform.release()}",
        "API.URL": "https://jsonplaceholder.typicode.com",
        "UI.URL": "https://www.saucedemo.com",
    }
    content = "\n".join(f"{key}={value}" for key, value in env.items())
    (Path(alluredir) / "environment.properties").write_text(content + "\n", encoding="utf-8")

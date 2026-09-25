import json

import allure
import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def _attach_to_allure(response, *args, **kwargs):
    """Прикладывает к отчёту каждый запрос и ответ."""
    request = response.request
    request_body = request.body.decode() if isinstance(request.body, bytes) else request.body
    allure.attach(
        f"{request.method} {request.url}\n\n{request_body or ''}",
        name=f"Request: {request.method} {request.path_url}",
        attachment_type=allure.attachment_type.TEXT,
    )
    try:
        body = json.dumps(response.json(), ensure_ascii=False, indent=2)
        attachment_type = allure.attachment_type.JSON
    except ValueError:
        body = response.text
        attachment_type = allure.attachment_type.TEXT
    allure.attach(body, name=f"Response: {response.status_code}", attachment_type=attachment_type)


@pytest.fixture(scope="session")
def api():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    session.hooks["response"].append(_attach_to_allure)
    yield session
    session.close()


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

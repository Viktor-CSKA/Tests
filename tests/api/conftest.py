import json

import allure
import pytest
import requests

from config import API_URL



def _format_headers(headers) -> str:
    return "\n".join(f"{name}: {value}" for name, value in headers.items())


def _format_body(body) -> str:
    if body is None:
        return ""
    if isinstance(body, bytes):
        body = body.decode(errors="replace")
    try:
        return json.dumps(json.loads(body), ensure_ascii=False, indent=2)
    except ValueError:
        return body


def _attach_to_allure(response, *args, **kwargs):
    """Прикладывает к отчёту каждый запрос и ответ целиком: заголовки, тело, время ответа."""
    request = response.request
    allure.attach(
        f"{request.method} {request.url}\n\n{_format_headers(request.headers)}\n\n{_format_body(request.body)}",
        name=f"Request: {request.method} {request.path_url}",
        attachment_type=allure.attachment_type.TEXT,
    )
    elapsed_ms = int(response.elapsed.total_seconds() * 1000)
    allure.attach(
        f"HTTP {response.status_code} {response.reason} — {elapsed_ms} ms\n\n"
        f"{_format_headers(response.headers)}\n\n{_format_body(response.content)}",
        name=f"Response: {response.status_code} {response.reason} ({elapsed_ms} ms)",
        attachment_type=allure.attachment_type.TEXT,
    )
    raw_body = request.body.decode(errors="replace") if isinstance(request.body, bytes) else request.body
    request_curl = " ".join(
        [f"curl -X {request.method} '{request.url}'"]
        + [f"-H '{name}: {value}'" for name, value in request.headers.items() if name != "Content-Length"]
        + ([f"-d '{raw_body}'"] if raw_body else [])
    )
    allure.attach(request_curl, name="cURL для повтора", attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope="session")
def api():
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    session.hooks["response"].append(_attach_to_allure)
    yield session
    session.close()


@pytest.fixture(scope="session")
def base_url():
    return API_URL

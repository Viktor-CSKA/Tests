import json

import allure
import requests


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


def attach_exchange(response: requests.Response, *args, **kwargs) -> None:
    """Прикладывает к Allure-отчёту запрос и ответ целиком: заголовки, тело, время ответа и cURL."""
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
    curl = " ".join(
        [f"curl -X {request.method} '{request.url}'"]
        + [f"-H '{name}: {value}'" for name, value in request.headers.items() if name != "Content-Length"]
        + ([f"-d '{raw_body}'"] if raw_body else [])
    )
    allure.attach(curl, name="cURL для повтора", attachment_type=allure.attachment_type.TEXT)


class BaseClient:
    """HTTP-клиент: общий базовый URL, таймаут и логирование каждого запроса в Allure."""

    timeout = 10

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json; charset=UTF-8"})
        self.session.hooks["response"].append(attach_exchange)

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, f"{self.base_url}{path}", **kwargs)

    def close(self) -> None:
        self.session.close()

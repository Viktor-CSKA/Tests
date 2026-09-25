# Портфолио автотестов

[![Allure Report](https://img.shields.io/badge/Allure-report-orange)](https://viktor-cska.github.io/Tests/)
[![Autotests](https://github.com/Viktor-CSKA/Tests/actions/workflows/tests.yml/badge.svg)](https://github.com/Viktor-CSKA/Tests/actions/workflows/tests.yml)

Здесь собраны мои автотесты: API и UI.

## Стек

- Python 3.11, pytest
- requests для API-тестов
- Playwright для UI-тестов, с паттерном Page Object
- Allure для отчётов
- GitHub Actions для CI: тесты запускаются на каждый push

## Структура

```
pages/            # Page Object для UI-тестов
tests/api/        # API-тесты (https://jsonplaceholder.typicode.com)
tests/ui/         # UI-тесты (https://www.saucedemo.com)
.github/workflows # CI
```

## Запуск локально

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                 # все тесты
pytest -m api          # только API
pytest -m ui --headed  # только UI, с открытым браузером
```

Адреса тестируемых систем можно переопределить переменными окружения `API_URL` и `UI_URL`,
например чтобы прогнать тесты на другом стенде.

## Отчёт Allure

Каждый прогон пишет результаты в `allure-results/` (настроено в `pytest.ini`).
В отчёте есть:

- группировка тестов по разделам: epic, feature, story;
- шаги тестов и Page Object, со скриншотом после каждого действия на странице;
- **ошибки, которые видит пользователь**: если на странице показана ошибка, её текст и скриншот попадают в отчёт, даже если тест прошёл;
- для каждого UI-теста — URL и скриншот в конце теста, консоль браузера, JS-ошибки и ошибки сети (4xx/5xx);
- для упавшего UI-теста дополнительно — HTML страницы, видео и Playwright trace (открывается на https://trace.playwright.dev);
- для API — полный запрос и ответ: заголовки, тело, статус, время ответа и cURL для повтора;
- вкладка Categories: падения разделены на дефекты продукта, ошибки в тестах и недоступность сервиса;
- блок Environment с окружением прогона.

Открыть отчёт локально (нужны [Allure CLI](https://allurereport.org/docs/install/) и Java):

```bash
pytest
allure serve allure-results
```

### Отчёт в CI

После каждого прогона в GitHub Actions HTML-отчёт сохраняется как артефакт `allure-report`
на странице запуска. При пуше в `main` отчёт вместе с историей прогонов публикуется
на GitHub Pages: https://viktor-cska.github.io/Tests/

Чтобы публикация заработала, один раз включите Pages:
**Settings → Pages → Source: Deploy from a branch → `gh-pages` / `(root)`**.
Ветка `gh-pages` появится после первого прогона на `main`.

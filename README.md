# Портфолио автотестов

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

## Отчёт Allure

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

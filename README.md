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

## Отчёт Allure

Каждый прогон пишет результаты в `allure-results/` (настроено в `pytest.ini`).
В отчёте есть:

- группировка тестов по разделам: epic, feature, story;
- шаги тестов и Page Object;
- запрос и ответ для каждого API-вызова;
- скриншот и HTML страницы для упавших UI-тестов;
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

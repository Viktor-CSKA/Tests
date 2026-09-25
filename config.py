import os

# Адреса тестируемых систем можно переопределить переменными окружения,
# например чтобы прогнать тесты на другом стенде.
API_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com").rstrip("/")
UI_URL = os.getenv("UI_URL", "https://www.saucedemo.com").rstrip("/")

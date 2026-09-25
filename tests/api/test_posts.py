import allure
import pytest

pytestmark = [pytest.mark.api, allure.epic("API"), allure.feature("Посты")]


@allure.story("Получение поста")
@allure.title("GET /posts/1 возвращает пост")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_post_returns_200(api, base_url):
    with allure.step("Запросить пост с id=1"):
        response = api.get(f"{base_url}/posts/1")

    with allure.step("Проверить статус и структуру ответа"):
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == 1
        assert {"userId", "id", "title", "body"} <= body.keys()


@allure.story("Получение поста")
@allure.title("GET несуществующего поста возвращает 404")
@allure.severity(allure.severity_level.NORMAL)
def test_get_nonexistent_post_returns_404(api, base_url):
    with allure.step("Запросить пост с несуществующим id"):
        response = api.get(f"{base_url}/posts/99999")

    with allure.step("Проверить статус 404"):
        assert response.status_code == 404


@allure.story("Создание поста")
@allure.title("POST /posts создаёт пост")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_post(api, base_url):
    payload = {"title": "portfolio", "body": "autotests", "userId": 1}

    with allure.step("Отправить запрос на создание поста"):
        response = api.post(f"{base_url}/posts", json=payload)

    with allure.step("Проверить статус 201 и данные в ответе"):
        assert response.status_code == 201
        body = response.json()
        for key, value in payload.items():
            assert body[key] == value
        assert "id" in body


@allure.story("Фильтрация постов")
@allure.title("Фильтрация постов по userId={user_id}")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_filter_posts_by_user(api, base_url, user_id):
    with allure.step(f"Запросить посты пользователя {user_id}"):
        response = api.get(f"{base_url}/posts", params={"userId": user_id})

    with allure.step("Проверить, что все посты принадлежат пользователю"):
        assert response.status_code == 200
        posts = response.json()
        assert posts
        assert all(post["userId"] == user_id for post in posts)

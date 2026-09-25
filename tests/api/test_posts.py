import allure
import pytest
from pydantic import TypeAdapter

from models.jsonplaceholder import Post

pytestmark = [pytest.mark.api, allure.epic("API"), allure.feature("Посты")]

POSTS = TypeAdapter(list[Post])


@allure.story("Получение постов")
class TestGetPosts:
    @pytest.mark.smoke
    @allure.title("Список постов соответствует контракту")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_matches_contract(self, jsonplaceholder):
        response = jsonplaceholder.get_posts()

        with allure.step("Статус 200, 100 постов, каждый соответствует схеме Post"):
            assert response.status_code == 200
            posts = POSTS.validate_python(response.json())
            assert len(posts) == 100

        with allure.step("Идентификаторы постов уникальны"):
            ids = [post.id for post in posts]
            assert len(ids) == len(set(ids))

    @pytest.mark.smoke
    @allure.title("Пост по id соответствует контракту")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_by_id(self, jsonplaceholder):
        response = jsonplaceholder.get_post(1)

        with allure.step("Статус 200 и пост с id=1"):
            assert response.status_code == 200
            assert Post.model_validate(response.json()).id == 1

    @allure.title("Фильтрация постов по userId={user_id}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("user_id", [1, 5, 10])
    def test_filter_by_user(self, jsonplaceholder, user_id):
        response = jsonplaceholder.get_posts(userId=user_id)

        with allure.step(f"Все посты принадлежат пользователю {user_id}"):
            assert response.status_code == 200
            posts = POSTS.validate_python(response.json())
            assert posts
            assert {post.userId for post in posts} == {user_id}

    @allure.title("Фильтр по несуществующему пользователю возвращает пустой список")
    @allure.severity(allure.severity_level.MINOR)
    def test_filter_by_unknown_user(self, jsonplaceholder):
        response = jsonplaceholder.get_posts(userId=9999)

        with allure.step("Статус 200 и пустой список"):
            assert response.status_code == 200
            assert response.json() == []

    @allure.title("Несуществующий пост (id={post_id}) возвращает 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("post_id", [0, 101, 99999])
    def test_not_found(self, jsonplaceholder, post_id):
        response = jsonplaceholder.get_post(post_id)

        with allure.step("Статус 404 и пустое тело"):
            assert response.status_code == 404
            assert response.json() == {}


@allure.story("Изменение постов")
class TestModifyPosts:
    @pytest.mark.smoke
    @allure.title("POST /posts создаёт пост")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create(self, jsonplaceholder, faker):
        payload = {"title": faker.sentence(), "body": faker.paragraph(), "userId": 1}

        response = jsonplaceholder.create_post(payload)

        with allure.step("Статус 201, в ответе переданные поля и новый id"):
            assert response.status_code == 201
            post = Post.model_validate(response.json())
            assert post.model_dump(exclude={"id"}) == payload
            assert post.id == 101

    @allure.title("PUT /posts/1 полностью заменяет пост")
    @allure.severity(allure.severity_level.NORMAL)
    def test_replace(self, jsonplaceholder, faker):
        payload = {"id": 1, "title": faker.sentence(), "body": faker.paragraph(), "userId": 1}

        response = jsonplaceholder.replace_post(1, payload)

        with allure.step("Статус 200 и пост совпадает с отправленным"):
            assert response.status_code == 200
            assert response.json() == payload

    @allure.title("PATCH /posts/1 меняет только переданное поле")
    @allure.severity(allure.severity_level.NORMAL)
    def test_partial_update(self, jsonplaceholder, faker):
        original = jsonplaceholder.get_post(1).json()
        new_title = faker.sentence()

        response = jsonplaceholder.update_post(1, {"title": new_title})

        with allure.step("Изменился только title, остальные поля прежние"):
            assert response.status_code == 200
            assert response.json() == {**original, "title": new_title}

    @allure.title("DELETE /posts/1 удаляет пост")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete(self, jsonplaceholder):
        response = jsonplaceholder.delete_post(1)

        with allure.step("Статус 200 и пустое тело"):
            assert response.status_code == 200
            assert response.json() == {}

    @allure.title("POST /posts с пустым телом создаёт пост только с id")
    @allure.description(
        "JSONPlaceholder не валидирует тело запроса. Тест фиксирует это поведение: "
        "если API начнёт валидацию, тест упадёт и сообщит об изменении контракта."
    )
    @allure.severity(allure.severity_level.MINOR)
    def test_create_with_empty_body(self, jsonplaceholder):
        response = jsonplaceholder.create_post({})

        with allure.step("Статус 201 и в ответе только id"):
            assert response.status_code == 201
            assert response.json() == {"id": 101}

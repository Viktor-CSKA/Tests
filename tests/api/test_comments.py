import allure
import pytest
from pydantic import TypeAdapter

from models.jsonplaceholder import Comment

pytestmark = [pytest.mark.api, allure.epic("API"), allure.feature("Комментарии")]

COMMENTS = TypeAdapter(list[Comment])


@allure.story("Комментарии к посту")
class TestComments:
    @pytest.mark.smoke
    @allure.title("Комментарии поста {post_id} соответствуют контракту")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("post_id", [1, 50, 100])
    def test_post_comments_contract(self, jsonplaceholder, post_id):
        response = jsonplaceholder.get_post_comments(post_id)

        with allure.step("Статус 200, у поста 5 комментариев, все относятся к нему"):
            assert response.status_code == 200
            comments = COMMENTS.validate_python(response.json())
            assert len(comments) == 5
            assert {comment.postId for comment in comments} == {post_id}

    @allure.title("Вложенный маршрут и фильтр по postId возвращают одинаковые данные")
    @allure.severity(allure.severity_level.NORMAL)
    def test_nested_route_equals_filter(self, jsonplaceholder):
        nested = jsonplaceholder.get_post_comments(1)
        filtered = jsonplaceholder.get_comments(postId=1)

        with allure.step("/posts/1/comments == /comments?postId=1"):
            assert nested.status_code == filtered.status_code == 200
            assert nested.json() == filtered.json()

    @allure.title("Всего 500 комментариев с уникальными id")
    @allure.severity(allure.severity_level.MINOR)
    def test_all_comments(self, jsonplaceholder):
        response = jsonplaceholder.get_comments()

        with allure.step("Статус 200, 500 комментариев, id уникальны"):
            assert response.status_code == 200
            comments = COMMENTS.validate_python(response.json())
            assert len(comments) == 500
            assert len({comment.id for comment in comments}) == 500

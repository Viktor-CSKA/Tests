import allure
import pytest
from pydantic import TypeAdapter

from models.jsonplaceholder import Todo, User

pytestmark = [pytest.mark.api, allure.epic("API"), allure.feature("Пользователи")]

USERS = TypeAdapter(list[User])
TODOS = TypeAdapter(list[Todo])


@allure.story("Профили пользователей")
class TestUsers:
    @pytest.mark.smoke
    @allure.title("Список пользователей соответствует контракту")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_list_matches_contract(self, jsonplaceholder):
        response = jsonplaceholder.get_users()

        with allure.step("Статус 200, 10 пользователей с полным профилем"):
            assert response.status_code == 200
            users = USERS.validate_python(response.json())
            assert len(users) == 10

        with allure.step("Логины и email уникальны"):
            assert len({user.username for user in users}) == 10
            assert len({user.email.lower() for user in users}) == 10

    @allure.title("Профиль пользователя {user_id} соответствует контракту")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("user_id", [1, 10])
    def test_get_by_id(self, jsonplaceholder, user_id):
        response = jsonplaceholder.get_user(user_id)

        with allure.step(f"Статус 200 и пользователь с id={user_id}"):
            assert response.status_code == 200
            assert User.model_validate(response.json()).id == user_id

    @allure.title("Несуществующий пользователь возвращает 404")
    @allure.severity(allure.severity_level.NORMAL)
    def test_not_found(self, jsonplaceholder):
        response = jsonplaceholder.get_user(11)

        with allure.step("Статус 404"):
            assert response.status_code == 404


@allure.story("Задачи пользователя")
class TestTodos:
    @allure.title("Задачи пользователя {user_id} соответствуют контракту")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("user_id", [1, 7])
    def test_user_todos(self, jsonplaceholder, user_id):
        response = jsonplaceholder.get_user_todos(user_id)

        with allure.step("Статус 200, 20 задач, все принадлежат пользователю"):
            assert response.status_code == 200
            todos = TODOS.validate_python(response.json())
            assert len(todos) == 20
            assert {todo.userId for todo in todos} == {user_id}

    @allure.title("Фильтр задач по статусу completed={completed}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("completed", [True, False], ids=["выполненные", "невыполненные"])
    def test_filter_by_status(self, jsonplaceholder, completed):
        all_todos = TODOS.validate_python(jsonplaceholder.get_user_todos(1).json())

        response = jsonplaceholder.get_user_todos(1, completed=str(completed).lower())

        with allure.step("Вернулись только задачи с нужным статусом, и ни одна не потерялась"):
            assert response.status_code == 200
            todos = TODOS.validate_python(response.json())
            assert todos
            assert {todo.completed for todo in todos} == {completed}
            assert len(todos) == sum(todo.completed == completed for todo in all_todos)

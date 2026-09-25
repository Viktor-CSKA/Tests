import allure
import requests

from clients.base import BaseClient


class JsonPlaceholderClient(BaseClient):
    """Клиент для https://jsonplaceholder.typicode.com — один метод на одну операцию API."""

    @allure.step("GET /posts")
    def get_posts(self, **params) -> requests.Response:
        return self.request("GET", "/posts", params=params)

    @allure.step("GET /posts/{post_id}")
    def get_post(self, post_id: int) -> requests.Response:
        return self.request("GET", f"/posts/{post_id}")

    @allure.step("POST /posts")
    def create_post(self, payload: dict) -> requests.Response:
        return self.request("POST", "/posts", json=payload)

    @allure.step("PUT /posts/{post_id}")
    def replace_post(self, post_id: int, payload: dict) -> requests.Response:
        return self.request("PUT", f"/posts/{post_id}", json=payload)

    @allure.step("PATCH /posts/{post_id}")
    def update_post(self, post_id: int, payload: dict) -> requests.Response:
        return self.request("PATCH", f"/posts/{post_id}", json=payload)

    @allure.step("DELETE /posts/{post_id}")
    def delete_post(self, post_id: int) -> requests.Response:
        return self.request("DELETE", f"/posts/{post_id}")

    @allure.step("GET /posts/{post_id}/comments")
    def get_post_comments(self, post_id: int) -> requests.Response:
        return self.request("GET", f"/posts/{post_id}/comments")

    @allure.step("GET /comments")
    def get_comments(self, **params) -> requests.Response:
        return self.request("GET", "/comments", params=params)

    @allure.step("GET /users")
    def get_users(self) -> requests.Response:
        return self.request("GET", "/users")

    @allure.step("GET /users/{user_id}")
    def get_user(self, user_id: int) -> requests.Response:
        return self.request("GET", f"/users/{user_id}")

    @allure.step("GET /users/{user_id}/todos")
    def get_user_todos(self, user_id: int, **params) -> requests.Response:
        return self.request("GET", f"/users/{user_id}/todos", params=params)

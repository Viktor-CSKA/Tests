import pytest

pytestmark = pytest.mark.api


def test_get_post_returns_200(api, base_url):
    response = api.get(f"{base_url}/posts/1")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert {"userId", "id", "title", "body"} <= body.keys()


def test_get_nonexistent_post_returns_404(api, base_url):
    response = api.get(f"{base_url}/posts/99999")

    assert response.status_code == 404


def test_create_post(api, base_url):
    payload = {"title": "portfolio", "body": "autotests", "userId": 1}

    response = api.post(f"{base_url}/posts", json=payload)

    assert response.status_code == 201
    body = response.json()
    for key, value in payload.items():
        assert body[key] == value
    assert "id" in body


@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_filter_posts_by_user(api, base_url, user_id):
    response = api.get(f"{base_url}/posts", params={"userId": user_id})

    assert response.status_code == 200
    posts = response.json()
    assert posts
    assert all(post["userId"] == user_id for post in posts)

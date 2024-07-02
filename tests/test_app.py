from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.models import User
from fast_zero.schemas import UserPublic


def test_create_user(client: TestClient):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_with_same_username(client: TestClient, user: User):
    response = client.post(
        '/users',
        json={
            'username': f'{user.username}',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_user_with_same_email(client: TestClient, user: User):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': f'{user.email}',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client: TestClient):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client: TestClient, user: User):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_read_user(client: TestClient, user: User):
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == UserPublic.model_validate(user).model_dump()


def test_read_user_not_found(client: TestClient, user: User):
    response = client.get(f'/users/{user.id + 1}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client: TestClient, user: User):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_user_not_found(client: TestClient, user: User):
    response = client.put(
        f'/users/{user.id + 1}',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client: TestClient, user: User):
    response = client.delete(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client: TestClient, user: User):
    response = client.delete(f'/users/{user.id + 1}')
    assert response.status_code == HTTPStatus.NOT_FOUND

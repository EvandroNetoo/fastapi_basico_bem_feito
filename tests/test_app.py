from http import HTTPStatus

from fastapi.testclient import TestClient


def test_root_deve_retornar_ok_e_ola_mundo(client: TestClient):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client: TestClient):
    response = client.post(
        '/users/',
        json={
            'username': 'Evandro',
            'email': 'evandro@gmail.com',
            'password': 'Abc!23',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'Evandro',
        'email': 'evandro@gmail.com',
    }


def test_read_users(client: TestClient):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'Evandro',
                'email': 'evandro@gmail.com',
            }
        ]
    }


def test_read_user(client: TestClient):
    response = client.get('/users/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Evandro',
        'email': 'evandro@gmail.com',
    }


def test_read_user_not_found(client: TestClient):
    response = client.get('/users/2/')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client: TestClient):
    response = client.put(
        '/users/1/',
        json={
            'username': 'Evandro Neto',
            'email': 'evandro.rsneto@gmail.com',
            'password': '!23Abc',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Evandro Neto',
        'email': 'evandro.rsneto@gmail.com',
    }


def test_update_user_not_found(client: TestClient):
    response = client.put(
        '/users/2/',
        json={
            'username': 'Evandro Neto',
            'email': 'evandro.rsneto@gmail.com',
            'password': '!23Abc',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client: TestClient):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client: TestClient):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND

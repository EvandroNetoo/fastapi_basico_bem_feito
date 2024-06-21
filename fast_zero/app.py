from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()


users: list[UserDB] = []


@app.get('/')
def read_root() -> Message:
    return Message(message='Olá Mundo!')


@app.post('/users/', status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema) -> UserPublic:
    user_db = UserDB(
        id=1 if len(users) == 0 else users[-1].id + 1,
        **user.model_dump(),
    )
    users.append(user_db)
    return user_db


@app.get('/users/')
def read_users() -> UserList:
    return {'users': users}


@app.get('/users/{user_id}/')
def read_user(user_id: int) -> UserPublic:
    user = list(filter(lambda user: user.id == user_id, users))
    if len(user) == 0:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'User not found')
    user = user[0]
    return user


@app.put('/users/{user_id}/')
def update_user(user_id: int, updated_user: UserSchema) -> UserPublic:
    user = list(filter(lambda user: user.id == user_id, users))
    if len(user) == 0:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'User not found')
    user = user[0]
    user_index = users.index(user)
    user_db = UserDB(id=user_id, **updated_user.model_dump())
    users[user_index] = user_db
    return user_db


@app.delete('/users/{user_id}/')
def delete_user(user_id: int) -> Message:
    user = list(filter(lambda user: user.id == user_id, users))
    if len(user) == 0:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'User not found')
    user = user[0]
    users.remove(user)
    return Message(message='User deleted')

from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from api.schemas.schemas import (
    HealthStatus,
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

database = []


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    """Comentários da API"""
    return {"message": "Olá mundo!"}


@app.get("/health", status_code=HTTPStatus.OK, response_model=HealthStatus)
def health():
    return {"status": "ok"}


@app.post("/user", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user)

    return user


@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserList)
def list_users():
    return {"users": database}


@app.put("/user/{user_id}")
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    updated_user = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = updated_user

    return updated_user


@app.delete("/user/{user_id}", response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 0:
        raise HTTPException(
            http_status=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    del database[user_id - 1]

    return {"message": "User deleted"}

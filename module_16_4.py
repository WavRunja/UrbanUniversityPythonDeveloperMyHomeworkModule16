# module_16_4.py

# Домашнее задание по теме "Модели данных Pydantic"

# Цель: научиться описывать и использовать Pydantic модель.

# Задача "Модель пользователя":
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List, Annotated

# Используйте CRUD запросы из предыдущей задачи.
app = FastAPI()

# Создайте пустой список users = []
users = []


# Создайте класс(модель) User, наследованный от BaseModel, который будет содержать следующие поля:
class User(BaseModel):
    # id - номер пользователя (int)
    id: int
    # username - имя пользователя (str)
    username: str
    # age - возраст пользователя (int)
    age: int


# Измените и дополните ранее описанные 4 CRUD запроса:
# get запрос по маршруту '/users' теперь возвращает список users.
@app.get("/users", response_model=List[User])
async def get_users():
    return users


# post запрос по маршруту '/user/{username}/{age}', теперь:
# 1. Добавляет в список users объект User.
# 2. id этого объекта будет на 1 больше, чем у последнего в списке users. Если список users пустой, то 1.
# 3. Все остальные параметры объекта User - переданные в функцию username и age соответственно.
# 4. В конце возвращает созданного пользователя.
@app.post("/user/{username}/{age}", response_model=User)
async def add_user(
    username: Annotated[str, Path(description="Enter username", min_length=5, max_length=20, example="UrbanUser")],
    age: Annotated[int, Path(description="Enter age", ge=18, le=120, example=24)]
):
    new_user_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_user_id, username=username, age=age)
    users.append(new_user)
    return new_user


# put запрос по маршруту '/user/{user_id}/{username}/{age}' теперь:
# 1. Обновляет username и age пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
# 2. В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием
# "User was not found" и кодом 404.
@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(
    user_id: Annotated[int, Path(description="Enter User ID", ge=1, le=100, example=1)],
    username: Annotated[str, Path(description="Enter username", min_length=5, max_length=20, example="UrbanProfi")],
    age: Annotated[int, Path(description="Enter age", ge=18, le=120, example=28)]
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


# delete запрос по маршруту '/user/{user_id}', теперь:
# Удаляет пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
# В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.
@app.delete("/user/{user_id}", response_model=User)
async def delete_user(
    user_id: Annotated[int, Path(description="Enter User ID", ge=1, le=100, example=2)]
):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# INFO:     127.0.0.1:52475 - "GET /docs HTTP/1.1" 200 OK
# INFO:     127.0.0.1:52475 - "GET /openapi.json HTTP/1.1" 200 OK
# INFO:     127.0.0.1:52477 - "GET /users HTTP/1.1" 200 OK
# INFO:     127.0.0.1:52478 - "POST /user/UrbanUser/24 HTTP/1.1" 200 OK
# INFO:     127.0.0.1:52479 - "GET /users HTTP/1.1" 200 OK
# INFO:     127.0.0.1:52493 - "POST /user/UrbanTest/36 HTTP/1.1" 200 OK
# INFO:     127.0.0.1:52497 - "POST /user/Admin/42 HTTP/1.1" 200 OK
# INFO:     127.0.0.1:52510 - "PUT /user/1/UrbanProfi/28 HTTP/1.1" 200 OK
# INFO:     127.0.0.1:52511 - "DELETE /user/2 HTTP/1.1" 200 OK
# INFO:     127.0.0.1:52512 - "DELETE /user/2 HTTP/1.1" 404 Not Found

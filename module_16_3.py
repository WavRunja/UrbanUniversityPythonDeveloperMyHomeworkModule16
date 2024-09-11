# module_16_3.py

# Домашнее задание по теме "CRUD Запросы: Get, Post, Put Delete."
# Цель: выработать навык работы с CRUD запросами.

# Задача "Имитация работы с БД".
from fastapi import FastAPI, Path
from typing import Annotated

# Создайте новое приложение FastAPI и сделайте CRUD запросы.
app = FastAPI()

# Создайте словарь users = {'1': 'Имя: Example, возраст: 18'}
users = {'1': 'Имя: Example, возраст: 18'}

# Реализуйте 4 CRUD запроса:
# get запрос по маршруту '/users', который возвращает словарь users.
@app.get("/users")
async def get_users():
    return users


# post запрос по маршруту '/user/{username}/{age}', который добавляет в словарь по максимальному по значению ключом
# значение строки "Имя: {username}, возраст: {age}". И возвращает строку "User <user_id> is registered".
@app.post("/user/{username}/{age}")
async def add_user(
    username: Annotated[str, Path(description="Enter username", min_length=5, max_length=20, example="UrbanUser")],
    age: Annotated[int, Path(description="Enter age", ge=18, le=120, example=24)]
):
    new_user_id = str(int(max(users.keys())) + 1)
    users[new_user_id] = f"Имя: {username}, возраст: {age}"
    return {"message": f"User {new_user_id} is registered"}


# put запрос по маршруту '/user/{user_id}/{username}/{age}', который обновляет значение из словаря users
# под ключом user_id на строку "Имя: {username}, возраст: {age}". И возвращает строку "The user <user_id> is registered"
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: Annotated[int, Path(description="Enter User ID", ge=1, le=100, example=1)],
    username: Annotated[str, Path(description="Enter username", min_length=5, max_length=20, example="UrbanProfi")],
    age: Annotated[int, Path(description="Enter age", ge=18, le=120, example=28)]
):
    user_id_str = str(user_id)
    if user_id_str in users:
        users[user_id_str] = f"Имя: {username}, возраст: {age}"
        return {"message": f"User {user_id_str} has been updated"}
    else:
        return {"error": f"User with ID {user_id_str} does not exist"}


# delete запрос по маршруту '/user/{user_id}', который удаляет из словаря users по ключу user_id пару.
@app.delete("/user/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path(description="Enter User ID", ge=1, le=100, example=2)]
):
    user_id_str = str(user_id)
    if user_id_str in users:
        del users[user_id_str]
        return {"message": f"User {user_id_str} has been deleted"}
    else:
        return {"error": f"User with ID {user_id_str} does not exist"}

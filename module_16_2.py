# module_16_2.py

# Домашнее задание по теме "Валидация данных".
# Цель: научится писать необходимую валидацию для вводимых данных при помощи классов Path и Annotated.

# Задача "Аннотация и валидация".
from fastapi import FastAPI, Path
from typing import Annotated

# Объект FastAPI
app = FastAPI()


# Маршрут к главной странице "/"
@app.get("/")
async def get_main_page():
    return {"message": "Главная страница"}


# Маршрут к странице администратора "/user/admin"
@app.get("/user/admin")
async def get_admin_page():
    return {"message": "Вы вошли как администратор"}


# Допишите валидацию для маршрутов из предыдущей задачи при помощи классов Path и Annotated:
# '/user/{user_id}' - функция, выполняемая по этому маршруту,
# принимает аргумент user_id, для которого необходимо написать следующую валидацию:
# 1. Должно быть целым числом
# 2. Ограничено по значению: больше или равно 1 и меньше либо равно 100.
# 3. Описание - 'Enter User ID'
# 4. Пример - '1' (можете подставить свой пример не противоречащий валидации)
@app.get("/user/{user_id}")
async def get_user_number(
    user_id: Annotated[int, Path(description="Enter User ID", ge=1, le=100, example=1)]
):
    return {"message": f"Вы вошли как пользователь № {user_id}"}


# '/user' замените на '/user/{username}/{age}' - функция, выполняемая по этому маршруту,
# принимает аргументы username и age, для которых необходимо написать следующую валидацию:
# 1. username - строка, age - целое число.
# 2. username ограничение по длине: больше или равно 5 и меньше либо равно 20.
# 3. age ограничение по значению: больше или равно 18 и меньше либо равно 120.
# 4. Описания для username и age - 'Enter username' и 'Enter age' соответственно.
# 5. Примеры для username и age - 'UrbanUser' и '24' соответственно.
# (можете подставить свои примеры не противоречащие валидации).
@app.get("/user/{username}/{age}")
async def get_user_info(
    username: Annotated[str, Path(description="Enter username", min_length=5, max_length=20, example="UrbanUser")],
    age: Annotated[int, Path(description="Enter age", ge=18, le=120, example=24)]
):
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}

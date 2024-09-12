# Домашнее задание по теме "Шаблонизатор Jinja 2."

# Цель: научиться взаимодействовать с шаблонами Jinja 2 и использовать их в запросах.

# Задача "Список пользователей в шаблоне".
from fastapi import FastAPI, HTTPException, Path, Request
from pydantic import BaseModel
from typing import List, Annotated, Optional
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


# Измените и дополните ранее описанные CRUD запросы:
# Напишите новый запрос по маршруту '/':
# 1. Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
# 2. TemplateResponse должен подключать ранее заготовленный шаблон 'users.html',
# а также передавать в него request и список users.
# Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
@app.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


# Измените get запрос по маршруту '/users' на '/users/{user_id}':
# 1. Функция по этому запросу теперь принимает аргумент request и user_id.
# 2. Вместо возврата объекта модели User, теперь возвращается объект TemplateResponse.
# 3. TemplateResponse должен подключать ранее заготовленный шаблон 'users.html',
# а также передавать в него request и одного из пользователей - user.
# Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_user_by_id(request: Request, user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User was not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})


# Добавление нового пользователя POST
@app.post("/user/{username}/{age}", response_model=User)
async def add_user(
    username: Annotated[str, Path(description="Enter username", min_length=5, max_length=20, example="UrbanUser")],
    age: Annotated[int, Path(description="Enter age", ge=18, le=120, example=24)]
):
    new_user_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_user_id, username=username, age=age)
    users.append(new_user)
    return new_user


# Обновление данных пользователя PUT
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


# Удаление пользователя DELETE
@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int):
    user = next((u for u in users if u.id == user_id), None)
    if user:
        users.remove(user)
        return user
    raise HTTPException(status_code=404, detail="User was not found")

# Создайте несколько пользователей при помощи post запроса со следующими данными:
# username - UrbanUser, age - 24
# username - UrbanTest, age - 22
# username - Capybara, age - 60

# INFO:     127.0.0.1:53526 - "POST /user/UrbanUser/24 HTTP/1.1" 200 OK
# INFO:     127.0.0.1:53527 - "POST /user/UrbanTest/22 HTTP/1.1" 200 OK
# INFO:     127.0.0.1:53528 - "POST /user/Capybara/60 HTTP/1.1" 200 OK

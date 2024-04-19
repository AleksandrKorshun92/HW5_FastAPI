# Создать API для добавления нового пользователя в базу данных. Приложение
# должно иметь возможность принимать POST запросы с данными нового
# пользователя и сохранять их в базу данных.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для добавления нового пользователя (метод POST).
# Реализуйте валидацию данных запроса и ответа.

from fastapi import FastAPI, HTTPException, Request
from typing import Optional
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    password: str

us1 = User(id=1, name="Petr", email="spaik@mail.ru", password="123_qwe")
us2 = User(id=2, name="Sasha", email="spawww@mail.ru", password="qwe")
us3 = User(id=3, name="Lena", email="lena@mail.ru", password="333222_")

users = [us1, us2, us3]

@app.get("/users/") # выводит список всех пользователей
async def read_users_all():
    return {"users": users}


@app.get("/users/{users_id}")
async def read_users_id(users_id: int):
    user = [us for us in users if us.id == users_id]
    return {f"Users {users_id}": user}

@app.post("/append/")
async def append_users(user_add: User):
    users.append(user_add)
    return {f"Users {user_add}": user_add}

@app.put("/put/{users_id}")
async def put_users(users_id: int, user_put: User):
    for i in range(len(users)):
        if users[i].id==users_id:
            users[i]=user_put
        else:
            return HTTPException(status_code=404, detail="User not bazadate")
    return user_put

@app.delete("/delete/{users_id}")
async def delet_users(users_id: int):
    for i in range(len(users)):
        if users[i].id==users_id:
            return {f"Users delete": users.pop(i)}
    return HTTPException(status_code=404, detail="User not bazadate")


@app.get("/start/")
async def read_item(request: Request):
    return templates.TemplateResponse("base.html", {"request": request, "users": users})

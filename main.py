
import models
from database import SessionLocal, engine
import uvicorn
from fastapi import FastAPI, Body, Depends

from sсhema import ItemSchema, UserSchema, UserLoginSchema, get_current_user
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from fastapi import HTTPException

models.Base.metadata.create_all(bind=engine)

items = [
    {
        "id": 1,
        "name": "Яблоки",
        "quantity": 134
    },
    {
        "id": 2,
        "name": "Бананы",
        "quantity": 103
    },
    {
        "id": 3,
        "name": "Груши",
        "quantity": 98
    },
]

users = []

app = FastAPI()



def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False



# route handlers

# testing
@app.get("/", tags=["test"])
def greet():
    return {"hello": "world!."}


# Get Posts
@app.get("/items", tags=["items"])
def get_posts():
    return { "data": items }


@app.get("/items/{id}", tags=["items"])
def get_single_post(id: int):
    if id > len(items):
        return {
            "error": "No such post with the supplied ID."
        }

    for item in items:
        if item["id"] == id:
            return {
                "data": item
            }


@app.post("/items", dependencies=[Depends(JWTBearer())], tags=["items"])
def add_item(item: ItemSchema,):
    user = get_current_user()
    if user.type == "seller":
        item.id = len(items) + 1
        items.append(item.dict())
        return {
            "data": "item added."
        }
    else:
        raise HTTPException(status_code=403, detail="Нет доступа")


@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
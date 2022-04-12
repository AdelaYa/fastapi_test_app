import uvicorn

from auth.auth_bearer import JWTBearer
from utils.service import get_user_by_token, get_item_by_id
from auth.auth_handler import signJWT
from utils.users import get_random_string, hash_password, validate_password
from db import get_db, engine
import models as models
import schemas as schemas
from repositories import ItemRepo, UserRepo, CartRepo
from sqlalchemy.orm import Session
from typing import List

from fastapi import FastAPI, Depends

from fastapi import HTTPException

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# testing
@app.get("/", tags=["test"])
def greet():
    return {"hello": "world!."}


@app.get('/items', tags=["Item"], response_model=List[schemas.Item])
def get_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all Items in database
    """
    all_items = ItemRepo.fetch_all(db, skip=skip, limit=limit)
    return all_items


@app.get('/items/{item_id}', tags=["Item"], response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get the Item with the given ID  in database
    """
    db_item = ItemRepo.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    return db_item


@app.post("/items", tags=["items"], response_model=schemas.Item, status_code=201)
async def add_item(item_request: schemas.ItemCreate, token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    """
    Create an Item in the database
    """
    get_user = get_user_by_token(token, db)
    if get_user.role != "seller":
        raise HTTPException(status_code=403, detail="Access denied ")
    return await ItemRepo.create(db=db, item=item_request)


@app.post("/cart")
async def add_item_to_cart(add_to_cart: schemas.AddToCart, token: str = Depends(JWTBearer()),
                           db: Session = Depends(get_db)):
    """
    Add an Item to a cart
    """
    get_user = get_user_by_token(token, db)
    selected_item = get_item_by_id(add_to_cart.product_id, db)

    if get_user.role != "buyer":
        raise HTTPException(status_code=403, detail="Access denied ")
    elif add_to_cart.quantity > selected_item.quantity or selected_item.quantity == 0:
        raise HTTPException(status_code=404, detail="Out of stock")
    else:
        selected_item.quantity -= add_to_cart.quantity
        return await CartRepo.create(db=db, item=add_to_cart)


@app.post("/user/signup", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create an User in the database
    """
    salt = get_random_string()
    user.password = f"{salt}${hash_password(user.password, salt)}"
    db_user = UserRepo.fetch_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await UserRepo.create(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all Users in database
    """
    users = UserRepo.fetch_all(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user_id(user_id: int, db: Session = Depends(get_db)):
    """
    Get the User with the given ID  in database
    """
    db_user = UserRepo.fetch_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/user/login")
def user_login(user_auth: schemas.UserLoginSchema, db: Session = Depends(get_db)):
    """
    Login
    """

    db_user = UserRepo.fetch_by_email(db, user_auth.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not validate_password(
            password=user_auth.password, hashed_password=db_user.password
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return signJWT(db_user.email)


@app.get("/user/me")
async def read_users_me(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    """
    Get the current User
    """
    get_user = get_user_by_token(token, db)
    return get_user

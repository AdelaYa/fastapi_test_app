import jwt
from pydantic import BaseModel, Field, EmailStr
from fastapi import Depends

from auth.auth_bearer import JWTBearer
from auth.auth_handler import  JWT_SECRET, JWT_ALGORITHM


class ItemBase(BaseModel):
    name: str
    quantity: int

    class Config:
        schema_extra = {
            "example": {
                "name": "Яблоки",
                "quantity": 100
            }
        }


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    firstname: str
    email: EmailStr
    password: str
    type: str


    class Config:
        schema_extra = {
            "example": {
                "firstname": "Ivan",
                "email": "ivanov@x.com",
                "password": "weakpassword",
                "type": "buyer"
            }
        }


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int


    class Config:
        orm_mode = True


# async def get_current_user(token: str = Depends(JWTBearer())):
#     payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], verify_signature=False)
#     return {
#         "email": payload.get("email")
#     }
#

#
# class UserLoginSchema(BaseModel):
#     email: EmailStr = Field(...)
#     password: str = Field(...)
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "email": "ivanov@x.com",
#                 "password": "weakpassword"
#             }
#         }
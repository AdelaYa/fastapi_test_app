import jwt
from pydantic import BaseModel, Field, EmailStr
from fastapi import Depends

from auth.auth_bearer import JWTBearer
from auth.auth_handler import  JWT_SECRET, JWT_ALGORITHM


class ItemSchema(BaseModel):
    id: int = Field(default=None)
    name: str = Field(default=None)
    quantity: int = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "name": "Яблоки",
                "quantity": 100
            }
        }


class UserSchema(BaseModel):
    firstname: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    type: str = Field(default=None)


    class Config:
        schema_extra = {
            "example": {
                "firstname": "Ivan",
                "email": "ivanov@x.com",
                "password": "weakpassword",
                "type": "buyer"
            }
        }


async def get_current_user(token: str = Depends(JWTBearer())):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], verify_signature=False)
    return {
        "email": payload.get("email")
    }



class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "ivanov@x.com",
                "password": "weakpassword"
            }
        }
from pydantic import BaseModel


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


class AddToCart(BaseModel):
    product_id: int
    quantity: int


class UserBase(BaseModel):
    firstname: str
    email: str
    role: str


    class Config:
        schema_extra = {
            "example": {
                "firstname": "Ivan",
                "email": "ivanov@x.com",
                "password": "weakpassword",
                "role": "buyer"
            }
        }


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True



class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "ivanov@x.com",
                "password": "weakpassword"
            }
        }




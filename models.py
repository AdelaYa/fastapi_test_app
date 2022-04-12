from sqlalchemy import Column, Integer, String
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    firstname = Column(String)
    password = Column(String)
    role = Column(String, index=True)

    def __repr__(self):
        return 'User(email=%s, firstname=%s, password=%s, role=%s)' % (self.email, self.firstname, self.password, self.role)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, index=True)

    def __repr__(self):
        return 'ItemModel(name=%s, quantity=%s)' % (self.name, self.quantity)

class Cart(Base):
    __tablename__ = "carts"

    product_id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, index=True)

    def __repr__(self):
        return 'CartModel(id=%s, quantity=%s)' % (self.id, self.quantity)

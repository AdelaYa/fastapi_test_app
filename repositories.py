from sqlalchemy.orm import Session

import models
import schemas



class ItemRepo:

    async def create(db: Session, item: schemas.ItemCreate):
        db_item = models.Item(name=item.name, quantity=item.quantity)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def fetch_by_id(db: Session, _id):
        return db.query(models.Item).filter(models.Item.id == _id).first()

    def fetch_by_name(db: Session, name):
        return db.query(models.Item).filter(models.Item.name == name).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Item).offset(skip).limit(limit).all()

    async def delete(db: Session, item_id):
        db_item = db.query(models.Item).filter_by(id=item_id).first()
        db.delete(db_item)
        db.commit()

    async def update(db: Session, item_data):
        updated_item = db.merge(item_data)
        db.commit()
        return updated_item


class UserRepo:

    async def create(db: Session, user: schemas.UserCreate):
        db_user = models.User(firstname=user.firstname, email=user.email, password=user.password, role=user.role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def fetch_by_id(db: Session, _id: int):
        return db.query(models.User).filter(models.User.id == _id).first()

    def fetch_by_role(db: Session, role: str):
        return db.query(models.User).filter(models.User.role == role).first()

    def fetch_by_email(db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()

    async def delete(db: Session, _id: int):
        db_user = db.query(models.User).filter_by(id=_id).first()
        db.delete(db_user)
        db.commit()

    async def update(db: Session, user_data):
        db.merge(user_data)
        db.commit()


class CartRepo:

    async def create(db: Session, item: schemas.AddToCart):
        db_item = models.Cart(product_id=item.product_id, quantity=item.quantity)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item


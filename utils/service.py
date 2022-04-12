from auth.auth_handler import decodeJWT

from fastapi import HTTPException
from starlette import status

from sqlalchemy.orm import Session
from repositories import UserRepo, ItemRepo


def get_user_by_token(token: str, db: Session):
    token_email = decodeJWT(token)
    current_user = UserRepo.fetch_by_email(db, email=token_email["email"])
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


def get_item_by_id(item_id: int, db: Session):
    current_item = ItemRepo.fetch_by_id(db, _id=item_id)

    if not current_item:
        raise HTTPException(status_code=404, detail="Not found")
    return current_item


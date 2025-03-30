from typing import Annotated
from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import User
from database import get_db
from security import authenticate_user, get_password_hash

from exceptions import UserAlreadyExists, NotFoundException
from schema import UserResponse, UserCreate, UserLogin

# Set up the templates

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_200_OK, response_model=UserResponse)
def register(
    request: Request, db: Annotated[Session, Depends(get_db)], user: UserCreate
):
    result = db.execute(select(User).where(User.email == user.email))
    user_res = result.scalars().first()

    if user_res:
        raise UserAlreadyExists(detail="User already exists!")

    hashed_password = get_password_hash(user.password)
    model = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        location=user.location,
        interests=user.interests,
    )

    db.add(model)
    db.commit()
    db.refresh(model)

    return model


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserResponse)
def login(
    request: Request,
    login_data: UserLogin,
    db: Annotated[Session, Depends(get_db)] = None,
):
    # Authenticate user
    user = authenticate_user(
        db, schema=User, email=login_data.email, password=login_data.password
    )

    if not user:
        raise NotFoundException(
            detail="User with the email or password does not exist!"
        )

    return user


@router.get("/me")
def profile(request: Request, db: Annotated[Session, Depends(get_db)], email: str):
    user = db.scalars(select(User).where(User.email == email)).first()
    return user

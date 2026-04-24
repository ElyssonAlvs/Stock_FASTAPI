from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.services import user_service, auth_service

router = APIRouter(prefix="/v1/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    return user_service.create_user(db, user.email, user.password)
    

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Annotated[Session, Depends(get_db)]):
    user = user_service.authenticate_user(db, data.email, data.password)

    if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                    detail="Invalid credentials")

    token = auth_service.create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/users", response_model=list[UserResponse])
def get_users(db: Annotated[Session, Depends(get_db)]):
    return user_service.get_all_users(db)


@router.get("/protected")
def protected(user: Annotated[object, Depends(auth_service.get_current_user)]):
    return {"user": user}
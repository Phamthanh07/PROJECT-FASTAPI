from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.db.database import get_db
from app.services import user_service
from app.core.sercurity import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = user_service.create_user(db=db, user_data=user_data)
    return new_user


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db=db, email=email, password=password)

    token = create_access_token({
        "sub": user.email,
        "id": user.id,
        "role": user.role
    })

    return {
        "message": "Đăng nhập thành công",
        "access_token": token,
        "token_type": "bearer",
        "data": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at
        }
    }

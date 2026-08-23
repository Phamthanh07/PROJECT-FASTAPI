from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user, RoleChecker
from app.services.user_service import get_users
from app.schemas.user import UserResponse


router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", dependencies=[Depends(RoleChecker(["ADMIN"]))])
def list_users(
    email: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db)
):
    return get_users(email, is_active, db)
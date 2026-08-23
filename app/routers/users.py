from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.dependencies.auth import get_current_user, RoleChecker

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", dependencies=[Depends(RoleChecker(["ADMIN"]))])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

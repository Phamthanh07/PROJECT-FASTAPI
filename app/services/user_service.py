from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.sercurity import hash_password, verify_password

def create_user(db: Session, user_data: UserCreate):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    hashed = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=hashed,
        role="USER",
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Email hoặc mật khẩu không chính xác")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Tài khoản đã bị khóa")

    return user

def get_users(email: str | None, is_active: bool | None, db: Session):
    query = db.query(User)

    if email:
        query = query.filter(User.email.like(f"%{email}%"))

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    users = query.all()

    # Không trả password_hash
    return [
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        for u in users
    ]

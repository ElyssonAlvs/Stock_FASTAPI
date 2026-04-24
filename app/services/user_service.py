from sqlalchemy.orm import Session
from app.models.user import User
from app.services.auth_service import hash_password


def create_user(db: Session, email: str, password: str):
    user = User(email=email, password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    from app.services.auth_service import verify_password

    if not verify_password(password, user.password):
        return None

    return user


def get_all_users(db: Session):
    return db.query(User).all()
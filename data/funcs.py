from data.models import *
from data.password_funcs import *

def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db, username: str, password: str):
    db_user = User(username=username, password=hash_password(password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_users(db):
    return db.query(User).all()

def login_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    if user and verify_password(password, user.password):
        return user
    return None
# sql/funcs.py
from sql.models import *
from sql.password_funcs import *

def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

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

def create_chat(db, user1_id: int, user2_id: int):
    existing = db.query(Chat).filter(
        ((Chat.user1_id == user1_id) & (Chat.user2_id == user2_id)) |
        ((Chat.user1_id == user2_id) & (Chat.user2_id == user1_id))
    ).first()

    if existing:
        return existing

    user1 = get_user_by_id(db, user1_id)
    user2 = get_user_by_id(db, user2_id)

    name = f"{user1.username} & {user2.username}"

    chat = Chat(user1_id=user1_id, user2_id=user2_id, name=name)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def delete_chat(db, chat_id: int):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        db.delete(chat)
        db.commit()

def get_chats_of_user(db, user_id: int):
    return db.query(Chat).filter((Chat.user1_id == user_id) | (Chat.user2_id == user_id)).all()

def get_messages_of_chat(db, chat_id: int):
    return db.query(Message)\
        .filter(Message.chat_id == chat_id)\
        .order_by(Message.id)\
        .all()

def send_message(db, chat_id: int, sender_id: int, content: str):
    message = Message(chat_id=chat_id, sender_id=sender_id, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
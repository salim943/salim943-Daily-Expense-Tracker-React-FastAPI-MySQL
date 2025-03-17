from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(day=user.day, date=user.date, amount=user.amount)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_todo(db: Session, user_id: int, todo: schemas.TodoCreate):
    existing_todo = db.query(models.Todo).filter(models.Todo.owner_id == user_id).first()
    if existing_todo:
        return None
    
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_users(db: Session):
    return db.query(models.User).all()

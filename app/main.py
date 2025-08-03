from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)

# Create Database Tables
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.post("/users/{user_id}/todos/", response_model=schemas.Todo)
def create_todo(user_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    created_todo = crud.create_todo(db, user_id, todo)
    if not created_todo:
        raise HTTPException(status_code=400, detail="User already has a todo")
    return created_todo

@app.get("/users/", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

from fastapi import FastAPI
from sklearn.linear_model import LinearRegression
import numpy as np

app = FastAPI()

@app.get("/predict-next-month-expense")
def predict_expense():
    # Dummy past data: total expenses per month
    months = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)  # e.g., Jan-May
    expenses = np.array([3000, 3200, 3500, 3700, 4000])  # in currency

    # Train linear regression model
    model = LinearRegression()
    model.fit(months, expenses)

    # Predict for next month (June = 6)
    next_month = 6
    predicted_expense = model.predict([[next_month]])[0]

    # Return as JSON
    return {
        "month": next_month,
        "predicted_expense": round(float(predicted_expense), 2)
    }

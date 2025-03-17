from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from . import crud, models, schemas
from .database import SessionLocal, engine
import numpy as np

#for admin page
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Insert initial data into the todos table, avoiding duplicates
def insert_initial_todos(db: Session):
    # Example user to associate the todos with (ensure a user exists)
    user = crud.get_user_by_email(db, email="user_x6@gmail.com")
    if not user:
        # Create a new user if one does not exist
        user = crud.create_user(db, schemas.UserCreate(email="user_x6@gmail.com", name="Evan", age=30))

    # Default todos to add
    default_todos = [
        schemas.TodoCreate(title="Buy groceries", description="Get milk, eggs, and bread."),
        schemas.TodoCreate(title="Read a book", description="Finish reading the book 'Atomic Habits'."),
        schemas.TodoCreate(title="Exercise", description="Go for a 30-minute run.")
    ]

    # Insert each todo if it doesn't already exist
    for todo in default_todos:
        existing_todo = crud.get_user_todo_by_title(db=db, user_id=user.id, title=todo.title)
        if not existing_todo:
            crud.create_user_todo(db=db, user_id=user.id, todo=todo)

# Ensure initial data is loaded on startup
with SessionLocal() as db:
    insert_initial_todos(db)
    
##########################for admin page################
# Token and authentication setup
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "password123"
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_admin(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username != ADMIN_CREDENTIALS["username"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != ADMIN_CREDENTIALS["username"] or form_data.password != ADMIN_CREDENTIALS["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Admin-protected route to insert user details and todos
@app.post("/admin/insert_user_with_todos")
def admin_insert_user_with_todos(
    payload: dict,
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin),
):
    # Extract user data from the payload
    user_data = payload.get("user")
    todos_data = payload.get("todos")

    if not user_data:
        return {"status": "error", "message": "User data is required."}

    if not todos_data or not isinstance(todos_data, list):
        return {"status": "error", "message": "A list of todos is required."}

    # Create or fetch the user
    user = crud.get_user_by_email(db, email=user_data["email"])
    if not user:
        user = crud.create_user(
            db,
            schemas.UserCreate(
                email=user_data["email"], name=user_data["name"], age=user_data["age"]
            ),
        )

    # Insert todos for the user
    inserted_todos = []
    for todo_data in todos_data:
        existing_todo = crud.get_user_todo_by_title(
            db=db, user_id=user.id, title=todo_data["title"]
        )
        if not existing_todo:
            new_todo = crud.create_user_todo(
                db, user_id=user.id, todo=schemas.TodoCreate(**todo_data)
            )
            inserted_todos.append(new_todo)

    return {
        "status": "success",
        "message": f"User '{user.name}' and {len(inserted_todos)} todos inserted successfully.",
    }

########################################################

# Simple Addition
def addition (p, q):
    return {p+q}

# DSBSC modulation function
def dsbsc_modulation(frequency, amplitude):
    fs = amplitude * 10                  
    x_values = np.linspace(0, 1, 10000)
    message_signal = np.sin(2 * np.pi * frequency * x_values)
    carrier_signal = np.cos(2 * np.pi * amplitude * x_values)
    dsbsc_modulated_signal = message_signal * carrier_signal
    return {"x": x_values.tolist(), "y": dsbsc_modulated_signal.tolist()}

# Define the router
router = APIRouter()

# Routes
@app.post("/users/", response_model=schemas.User)
def post_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/usernames/", response_model=list[str])
def get_usernames(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    usernames = [user.name for user in users]
    return usernames
    
@app.get("/users/{user_id}/", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
    

@app.post("/users/{user_id}/todos/", response_model=schemas.Todo)
def post_todo_for_user(user_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_user_todo(db=db, user_id=user_id, todo=todo)

@app.get("/todos/", response_model=list[schemas.Todo])
def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

@app.get("/test")
async def get_test():
    return {"message": "Hello from FastAPI"}

# DSBSC modulation endpoint
@router.get("/process_data_dsbsc")
async def process_data_dsbsc(
    frequency: float = Query(1.0, description="Frequency for sine wave"),
    amplitude: float = Query(1.0, description="Amplitude for sine wave")
):
    sin_wave_data_dsbsc = dsbsc_modulation(frequency, amplitude)
    return {"sinWaveDatadsbsc": sin_wave_data_dsbsc, "messageFrequency": frequency, "carrierFrequency": amplitude}

# addition endpoint
@router.get("/process_data_addition")
async def process_data_addition(
    p: float = Query(1.0, description="first number"),
    q: float = Query(1.0, description="second number")
):
    r = addition(p,q)
    return {"r": r}
    
@app.get("/notes")
def get_notes():
    return {"notes": ["Note 1", "Note 2"]}
    
    
# Include the router
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

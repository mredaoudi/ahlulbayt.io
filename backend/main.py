# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import sqlite3
from sqlite3 import Connection
import uuid

# Setup
app = FastAPI()
SECRET_KEY = "secret-key"  # Change in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database setup
def get_db():
    conn = sqlite3.connect("app.db")
    try:
        yield conn
    finally:
        conn.close()

# Create tables on startup
with sqlite3.connect("app.db") as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        first_name TEXT,
        last_name TEXT,
        hashed_password TEXT,
        is_active BOOLEAN DEFAULT 0
    )""")
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS folders (
        id TEXT PRIMARY KEY,
        name TEXT,
        owner_id TEXT,
        parent_id TEXT NULL,
        FOREIGN KEY(owner_id) REFERENCES users(id),
        FOREIGN KEY(parent_id) REFERENCES folders(id)
    )""")
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        content TEXT,  # Storing as JSON string
        owner_id TEXT,
        folder_id TEXT NULL,
        FOREIGN KEY(owner_id) REFERENCES users(id),
        FOREIGN KEY(folder_id) REFERENCES folders(id)
    )""")
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS bookmarks (
        id TEXT PRIMARY KEY,
        link TEXT,
        owner_id TEXT,
        FOREIGN KEY(owner_id) REFERENCES users(id)
    )""")
    conn.commit()

# Auth setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str

class UserInDB(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class DocumentCreate(BaseModel):
    content: dict
    folder_id: Optional[str] = None

class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[str] = None

class BookmarkCreate(BaseModel):
    link: str

# Auth utilities
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Connection = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.execute(
        "SELECT id, username, first_name, last_name, is_active FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return UserInDB(**dict(zip(["id", "username", "first_name", "last_name", "is_active"], user)))

# Auth endpoints
@app.post("/register", response_model=UserInDB)
def register(user: UserCreate, db: Connection = Depends(get_db)):
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user.password)
    
    try:
        db.execute(
            "INSERT INTO users (id, username, first_name, last_name, hashed_password, is_active) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, user.username, user.first_name, user.last_name, hashed_password, False)
        )
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    return UserInDB(
        id=user_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=False
    )

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Connection = Depends(get_db)):
    user = db.execute(
        "SELECT username, hashed_password, is_active FROM users WHERE username = ?",
        (form_data.username,)
    ).fetchone()
    
    if not user or not verify_password(form_data.password, user[1]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if not user[2]:  # is_active
        raise HTTPException(status_code=400, detail="User not activated")
    
    access_token = create_access_token(data={"sub": user[0]})
    return {"access_token": access_token, "token_type": "bearer"}

# Document endpoints
@app.post("/documents", status_code=status.HTTP_201_CREATED)
def create_document(
    doc: DocumentCreate,
    user: UserInDB = Depends(get_current_user),
    db: Connection = Depends(get_db)
):
    doc_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO documents (id, content, owner_id, folder_id) VALUES (?, ?, ?, ?)",
        (doc_id, str(doc.content), user.id, doc.folder_id)
    )
    db.commit()
    return {"id": doc_id}

# Add similar CRUD endpoints for folders and bookmarks following the same pattern

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
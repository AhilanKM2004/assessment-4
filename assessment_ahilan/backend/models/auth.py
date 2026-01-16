from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.hash import argon2
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.deps import get_db
from datetime import datetime, timedelta

from models.model import users


SECRET_KEY = "blabblabla"   
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth = OAuth2PasswordBearer(tokenUrl="login")

# -------------------------------------------------------------------------- TOKEN

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def login_user(db: Session,email : str , password : str):
    person = db.query(users).filter(users.email ==email).first()

    if not person:
        raise HTTPException(status_code=404, detail="User not found")

    if not argon2.verify(password, person.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": person.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }



def get_current_user(token: str = Depends(auth),db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")

    user = db.query(users).filter(users.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

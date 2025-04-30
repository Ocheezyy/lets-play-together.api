from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from db import get_session
from sqlmodel import Session, select
from models import User
from globals import AUTH_SECRET_KEY


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.id == user_id)).first()
    if user is None:
        raise credentials_exception

    return user

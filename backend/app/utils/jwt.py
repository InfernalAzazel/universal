from datetime import timedelta, datetime
from typing import Optional

from jose import jwt

from app.settings import JWT_SECRET, JWT_ALGORITHM


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, JWT_ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str):
    return jwt.decode(token, JWT_SECRET, [JWT_ALGORITHM])

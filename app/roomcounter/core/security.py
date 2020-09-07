from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

from roomcounter.core.config import settings

SECRET_KEY = "c902190dc53dba745b1905dcec36aec84212eaab2992ce2eff0078e5bfde0082"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_hashed_pw(password):
    return pwd_context.hash(password)


def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,
                             settings.SECRET_KEY,
                             algorithm=ALGORITHM)
    return encoded_jwt

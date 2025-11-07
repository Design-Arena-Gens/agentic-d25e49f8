from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Tuple
from jose import jwt
from passlib.context import CryptContext
import uuid

from .config import settings

password_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def create_access_token(subject: str, jti: Optional[str] = None, expires_minutes: Optional[int] = None) -> Tuple[str, str]:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes or settings.access_token_expire_minutes)
    jti_val = jti or str(uuid.uuid4())
    to_encode = {"sub": subject, "exp": expire, "iat": now, "type": "access", "jti": jti_val}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt, jti_val


def create_refresh_token(subject: str, jti: Optional[str] = None, expires_days: Optional[int] = None) -> Tuple[str, str]:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=expires_days or settings.refresh_token_expire_days)
    jti_val = jti or str(uuid.uuid4())
    to_encode = {"sub": subject, "exp": expire, "iat": now, "type": "refresh", "jti": jti_val}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt, jti_val


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])

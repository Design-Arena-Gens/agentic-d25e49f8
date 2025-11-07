from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import EmailStr

from ..core.database import get_db
from ..core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from ..models.user import User
from ..models.token import RefreshToken, RevokedToken
from ..schemas.user import UserCreate, UserLogin, UserOut
from ..schemas.auth import TokenPair, TokenRefreshRequest, LogoutRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter((User.email == user_in.email) | (User.username == user_in.username)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or username already registered")
    user = User(
        username=user_in.username,
        email=str(user_in.email),
        password_hash=get_password_hash(user_in.password),
        preferences={},
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenPair)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == str(login_in.email)).first()
    if not user or not verify_password(login_in.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token, access_jti = create_access_token(str(user.id))
    refresh_token, refresh_jti = create_refresh_token(str(user.id))

    db.add(RefreshToken(user_id=user.id, jti=refresh_jti, revoked=False))
    db.commit()

    return TokenPair(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=TokenPair)
def refresh(req: TokenRefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_token(req.refresh_token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    jti = payload.get("jti")
    rt = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    if not rt or rt.revoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked or unknown")

    user_id = payload.get("sub")
    # Rotate refresh token
    new_access, new_access_jti = create_access_token(user_id)
    new_refresh, new_refresh_jti = create_refresh_token(user_id)

    rt.revoked = True
    db.add(rt)
    db.add(RefreshToken(user_id=int(user_id), jti=new_refresh_jti, revoked=False))
    db.commit()

    return TokenPair(access_token=new_access, refresh_token=new_refresh)

@router.post("/logout")
def logout(req: LogoutRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_token(req.refresh_token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    jti = payload.get("jti")
    rt = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    if not rt or rt.revoked:
        # idempotent
        return {"detail": "Logged out"}
    rt.revoked = True
    db.add(rt)
    db.commit()
    return {"detail": "Logged out"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError
from app.database import get_db
from app.models.models import User
from app.schemas.auth import UserRegister, UserLogin, TokenOut, RefreshTokenIn, UserOut
from app.configs.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)
from app.configs.dependencies import get_current_active_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """
    Create a new user account.
    Passwords are hashed with bcrypt before storage — plain text never touches the DB.
    """
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenOut)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate with username + password.
    Returns a short-lived access token and a long-lived refresh token.
    The access token is used in the Authorization header for all protected routes.
    The refresh token is used ONLY at /auth/refresh to get a new access token.
    """
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    if user.is_active != "true":
        raise HTTPException(status_code=403, detail="Account is inactive")

    token_data = {"sub": user.username}
    return TokenOut(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )


@router.post("/refresh", response_model=TokenOut)
def refresh_token(payload: RefreshTokenIn, db: Session = Depends(get_db)):
    """
    Exchange a valid refresh token for a new access + refresh token pair.
    This lets users stay logged in beyond the short access token window
    without re-entering their password.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
    )
    try:
        token_data = decode_token(payload.refresh_token)
        if token_data.get("type") != "refresh":
            raise credentials_exception
        username: str = token_data.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise credentials_exception

    new_data = {"sub": user.username}
    return TokenOut(
        access_token=create_access_token(new_data),
        refresh_token=create_refresh_token(new_data),
    )


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_active_user)):
    """
    Returns the currently authenticated user's profile.
    Useful for frontend session bootstrapping on page load.
    """
    return current_user
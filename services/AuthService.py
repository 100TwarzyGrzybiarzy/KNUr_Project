from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

from repositories.UserRepository import userRepository
from models.models import Token, TokenData, RefreshTokenRequest # Updated Pydantic imports
from schema.schema import User as UserModel # SQLAlchemy model aliased
from utils.security import verify_password, create_access_token, create_refresh_token, verify_token
from database import get_db
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class AuthService:

    def login_for_access_token(self, db: Session, form_data: OAuth2PasswordRequestForm = Depends()):
        user = userRepository.get_user_by_username(db, username=form_data.username)
        if not user or not verify_password(form_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        refresh_token = create_refresh_token(data={"sub": user.username})
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

    def refresh_access_token(self, db: Session, refresh_request: RefreshTokenRequest):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials or invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            token_type = jwt.decode(refresh_request.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_aud": False, "verify_iss": False, "verify_sub": False}).get("type")
            if token_type != "refresh":
                raise credentials_exception

            payload = verify_token(refresh_request.refresh_token, credentials_exception)
            username: str = payload.username # type: ignore
            if username is None:
                raise credentials_exception
        except Exception:
             raise credentials_exception

        user = userRepository.get_user_by_username(db, username=username)
        if user is None:
            raise credentials_exception

        new_access_token = create_access_token(data={"sub": user.username})
        return Token(access_token=new_access_token, refresh_token=refresh_request.refresh_token, token_type="bearer")

    def get_current_user_dependency(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload_check = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_exp": False, "verify_aud": False, "verify_iss": False, "verify_sub": False})
            if payload_check.get("type") != "access":
                 raise credentials_exception

            token_data = verify_token(token, credentials_exception)
            if token_data.username is None:
                 raise credentials_exception
        except Exception:
            raise credentials_exception

        user = userRepository.get_user_by_username(db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

authService = AuthService()
get_current_user = authService.get_current_user_dependency
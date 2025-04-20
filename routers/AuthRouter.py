from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models.models import Token, RefreshTokenRequest 
from services.AuthService import authService
from database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/token", response_model=Token)
async def login_for_access_token_route(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    return authService.login_for_access_token(db=db, form_data=form_data)

@router.post("/refresh", response_model=Token)
async def refresh_token_route(refresh_request: RefreshTokenRequest, db: Session = Depends(get_db)):
    return authService.refresh_access_token(db=db, refresh_request=refresh_request)
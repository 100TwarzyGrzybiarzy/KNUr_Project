from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from models.models import User, UserCreate, UserUpdate, Drug as DrugResponseModel, PatientFollowRequest
from schema.schema import User as UserModel
from services.UserService import userService
from services.AuthService import get_current_user
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return userService.create_new_user(db=db, user=user)


@router.get("/me", response_model=User, dependencies=[Depends(get_current_user)])
async def read_users_me_route(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=User, dependencies=[Depends(get_current_user)])
def read_user_route(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_user = userService.read_user(db=db, user_id=user_id)
    return db_user

@router.get("/", response_model=List[User], dependencies=[Depends(get_current_user)])
def read_users_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    users = userService.read_users(db=db, skip=skip, limit=limit)
    return users

@router.put("/{user_id}", response_model=User, dependencies=[Depends(get_current_user)])
def update_user_route(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return userService.update_existing_user(db=db, user_id=user_id, user_update=user, current_user=current_user)

@router.delete("/{user_id}", response_model=User, dependencies=[Depends(get_current_user)])
def delete_user_route(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return userService.delete_existing_user(db=db, user_id=user_id, current_user=current_user)


@router.post("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
def follow_drug_route(user_id: int, follow_request: PatientFollowRequest, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    userService.follow_drug(db=db, user_id=user_id, drug_id=follow_request.drug_id, current_user=current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{user_id}/follow/{drug_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
def unfollow_drug_route(user_id: int, drug_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    userService.unfollow_drug(db=db, user_id=user_id, drug_id=drug_id, current_user=current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{user_id}/followed_drugs", response_model=List[DrugResponseModel], dependencies=[Depends(get_current_user)])
def get_followed_drugs_route(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    drugs_db = userService.get_followed_drugs(db=db, user_id=user_id, current_user=current_user)
    return drugs_db
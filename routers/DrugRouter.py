from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.models import Drug, DrugCreate, DrugUpdate 
from schema.schema import User as UserModel
from services.DrugService import drugService
from services.AuthService import get_current_user
from database import get_db

router = APIRouter(
    prefix="/drugs",
    tags=["Drugs"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=Drug, status_code=status.HTTP_201_CREATED)
def create_drug_route(drug: DrugCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return drugService.create_new_drug(db=db, drug=drug, current_user=current_user)

@router.get("/{drug_id}", response_model=Drug)
def read_drug_route(drug_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_drug = drugService.read_drug(db=db, drug_id=drug_id)
    return db_drug

@router.get("/", response_model=List[Drug])
def read_drugs_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    drugs = drugService.read_drugs(db=db, skip=skip, limit=limit)
    return drugs

@router.put("/{drug_id}", response_model=Drug)
def update_drug_route(drug_id: int, drug: DrugUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return drugService.update_existing_drug(db=db, drug_id=drug_id, drug_update=drug, current_user=current_user)

@router.delete("/{drug_id}", response_model=Drug)
def delete_drug_route(drug_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return drugService.delete_existing_drug(db=db, drug_id=drug_id, current_user=current_user)
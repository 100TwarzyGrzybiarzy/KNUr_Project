from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from repositories.DrugRepository import drugRepository
from models.models import DrugCreate, DrugUpdate, Drug # Updated Pydantic imports
from schema.schema import Drugs as DrugModel # SQLAlchemy model aliased
from schema.schema import User as UserModel # SQLAlchemy User model

class DrugService:

    def create_new_drug(self, db: Session, drug: DrugCreate, current_user: UserModel) -> DrugModel:
        return drugRepository.create_drug(db=db, drug=drug)

    def read_drug(self, db: Session, drug_id: int) -> Optional[DrugModel]:
        db_drug = drugRepository.get_drug(db, drug_id=drug_id)
        if db_drug is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drug not found")
        return db_drug

    def read_drugs(self, db: Session, skip: int = 0, limit: int = 100) -> List[DrugModel]:
        return drugRepository.get_drugs(db, skip=skip, limit=limit)

    def update_existing_drug(self, db: Session, drug_id: int, drug_update: DrugUpdate, current_user: UserModel) -> Optional[DrugModel]:
        updated_drug = drugRepository.update_drug(db=db, drug_id=drug_id, drug_update=drug_update)
        if updated_drug is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drug not found")
        return updated_drug

    def delete_existing_drug(self, db: Session, drug_id: int, current_user: UserModel) -> Optional[DrugModel]:
        deleted_drug = drugRepository.delete_drug(db=db, drug_id=drug_id)
        if deleted_drug is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drug not found")
        return deleted_drug

drugService = DrugService()
from sqlalchemy.orm import Session
from typing import Optional, List
from schema.schema import Drugs
from models.models import DrugCreate, DrugUpdate

class DrugRepository:

    def get_drug(self, db: Session, drug_id: int) -> Optional[Drugs]:
        return db.query(Drugs).filter(Drugs.id == drug_id).first()

    def get_drugs(self, db: Session, skip: int = 0, limit: int = 100) -> List[Drugs]:
        return db.query(Drugs).offset(skip).limit(limit).all()

    def create_drug(self, db: Session, drug: DrugCreate) -> Drugs:
        db_drug = Drugs(**drug.model_dump())
        db.add(db_drug)
        db.commit()
        db.refresh(db_drug)
        return db_drug

    def update_drug(self, db: Session, drug_id: int, drug_update: DrugUpdate) -> Optional[Drugs]:
        db_drug = self.get_drug(db, drug_id)
        if not db_drug:
            return None

        update_data = drug_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
             setattr(db_drug, key, value)

        db.add(db_drug)
        db.commit()
        db.refresh(db_drug)
        return db_drug

    def delete_drug(self, db: Session, drug_id: int) -> Optional[Drugs]:
        db_drug = self.get_drug(db, drug_id)
        if db_drug:
            db.delete(db_drug)
            db.commit()
            return db_drug
        return None

drugRepository = DrugRepository()
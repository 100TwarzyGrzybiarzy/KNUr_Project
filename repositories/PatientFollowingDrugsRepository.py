from sqlalchemy.orm import Session
from typing import Optional, List
from schema.schema import PatientFollowingDrugs, Drugs

class PatientFollowingDrugsRepository:

    def is_following(self, db: Session, user_id: int, drug_id: int) -> bool:
        return db.query(PatientFollowingDrugs).filter(
            PatientFollowingDrugs.user_id == user_id,
            PatientFollowingDrugs.drug_id == drug_id
        ).first() is not None

    def follow_drug(self, db: Session, user_id: int, drug_id: int) -> Optional[PatientFollowingDrugs]:
        if not self.is_following(db, user_id, drug_id):
            db_follow = PatientFollowingDrugs(user_id=user_id, drug_id=drug_id)
            db.add(db_follow)
            db.commit()
            db.refresh(db_follow)
            return db_follow
        return db.query(PatientFollowingDrugs).filter(
            PatientFollowingDrugs.user_id == user_id,
            PatientFollowingDrugs.drug_id == drug_id
        ).first()


    def unfollow_drug(self, db: Session, user_id: int, drug_id: int) -> bool:
        db_follow = db.query(PatientFollowingDrugs).filter(
            PatientFollowingDrugs.user_id == user_id,
            PatientFollowingDrugs.drug_id == drug_id
        ).first()
        if db_follow:
            db.delete(db_follow)
            db.commit()
            return True
        return False

    def get_followed_drugs_by_user(self, db: Session, user_id: int) -> List[Drugs]:
         followed_assoc = db.query(PatientFollowingDrugs.drug_id).filter(PatientFollowingDrugs.user_id == user_id).all()
         followed_drug_ids = [item.drug_id for item in followed_assoc]
         if not followed_drug_ids:
             return []
         return db.query(Drugs).filter(Drugs.id.in_(followed_drug_ids)).all()

patientFollowingDrugsRepository = PatientFollowingDrugsRepository()
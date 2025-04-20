from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from repositories.UserRepository import userRepository
from repositories.PatientFollowingDrugsRepository import patientFollowingDrugsRepository
from models.models import UserCreate, UserUpdate, User, Drug as DrugModelPydantic # Updated Pydantic imports
from schema.schema import User as UserModel # SQLAlchemy model aliased
from schema.schema import Drugs as DrugModelDb # SQLAlchemy model aliased

class UserService:

    def create_new_user(self, db: Session, user: UserCreate) -> UserModel:
        db_user_by_username = userRepository.get_user_by_username(db, username=user.username)
        if db_user_by_username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
        db_user_by_email = userRepository.get_user_by_email(db, email=user.email)
        if db_user_by_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        return userRepository.create_user(db=db, user=user)

    def read_user(self, db: Session, user_id: int) -> Optional[UserModel]:
        db_user = userRepository.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return db_user

    def read_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[UserModel]:
        return userRepository.get_users(db, skip=skip, limit=limit)

    def update_existing_user(self, db: Session, user_id: int, user_update: UserUpdate, current_user: UserModel) -> Optional[UserModel]:
        target_user = self.read_user(db, user_id) # Check existence first

        if user_id != current_user.id and current_user.type != "admin":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")

        if user_update.username and user_update.username != target_user.username:
             existing = userRepository.get_user_by_username(db, user_update.username)
             if existing and existing.id != user_id:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
        if user_update.email and user_update.email != target_user.email:
            existing = userRepository.get_user_by_email(db, user_update.email)
            if existing and existing.id != user_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        updated_user = userRepository.update_user(db=db, user_id=user_id, user_update=user_update)

        return updated_user

    def delete_existing_user(self, db: Session, user_id: int, current_user: UserModel) -> Optional[UserModel]:
        target_user = self.read_user(db, user_id)

        if user_id != current_user.id and current_user.type != "admin":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")

        deleted_user = userRepository.delete_user(db=db, user_id=user_id)
        return deleted_user

    def follow_drug(self, db: Session, user_id: int, drug_id: int, current_user: UserModel) -> None:
         if user_id != current_user.id and current_user.type != "admin":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
         drug = db.query(DrugModelDb).filter(DrugModelDb.id == drug_id).first()
         if not drug:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drug not found")
         follow = patientFollowingDrugsRepository.follow_drug(db, user_id, drug_id)
         if follow is None:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not follow drug")

    def unfollow_drug(self, db: Session, user_id: int, drug_id: int, current_user: UserModel) -> None:
         if user_id != current_user.id and current_user.type != "admin":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

         removed = patientFollowingDrugsRepository.unfollow_drug(db, user_id, drug_id)
         if not removed:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not following this drug")

    def get_followed_drugs(self, db: Session, user_id: int, current_user: UserModel) -> List[DrugModelDb]:
         if user_id != current_user.id and current_user.type != "admin":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

         return patientFollowingDrugsRepository.get_followed_drugs_by_user(db, user_id)

userService = UserService()
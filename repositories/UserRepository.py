from sqlalchemy.orm import Session
from typing import Optional, List
from schema.schema import User
from models.models import UserCreate, UserUpdate
from utils.security import get_password_hash

class UserRepository:

    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            password_hash=hashed_password,
            type=user.type
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        db_user = self.get_user(db, user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)

        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            update_data["password_hash"] = hashed_password
            del update_data["password"]
        elif "password" in update_data:
             del update_data["password"]

        if 'password_hash' in update_data and "password_hash" not in user_update.model_fields_set:
             del update_data['password_hash']


        for key, value in update_data.items():
            setattr(db_user, key, value)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, user_id: int) -> Optional[User]:
        db_user = self.get_user(db, user_id)
        if db_user:
            db.delete(db_user)
            db.commit()
            return db_user
        return None

userRepository = UserRepository()
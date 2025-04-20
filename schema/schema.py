from sqlalchemy import (
    Column, Integer, String, ForeignKey, Date, Enum as SQLEnum,
    PrimaryKeyConstraint, MetaData
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.models import RemoveStatusEnum
Base = declarative_base()

connection_string = f"postgresql://postgres:michalpala123!@db.tniyxefccdtpsnfuxidc.supabase.co:5432/postgres"



class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    type = Column(String, nullable=False)
    pharmacy_warehouses = relationship("PharmacyWarehouse", back_populates="owner")
    followed_drugs_association = relationship("PatientFollowingDrugs", back_populates="user")

class Drugs(Base):
    __tablename__ = "Drugs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    batch_number = Column(String)
    active_substance = Column(String)
    remove_status = Column(SQLEnum(RemoveStatusEnum, name="remove_status_enum"), nullable=False, default=RemoveStatusEnum.aktywny)
    description = Column(String)
    date = Column(Date)
    warehouse_association = relationship("PharmacyWarehouseDrugsJoin", back_populates="drug")
    followed_by_users_association = relationship("PatientFollowingDrugs", back_populates="drug")

class PharmacyWarehouse(Base):
    __tablename__ = "pharmacy_warehouse"
    pharmacy_warehouse_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    name = Column(String, nullable=False)
    localization = Column(String)
    owner = relationship("User", back_populates="pharmacy_warehouses")
    drugs_association = relationship("PharmacyWarehouseDrugsJoin", back_populates="pharmacy_warehouse")

class PharmacyWarehouseDrugsJoin(Base):
    __tablename__ = "pharmacy_warehouse_drugs_join"
    pharmacy_warehouse_id = Column(Integer, ForeignKey("pharmacy_warehouse.pharmacy_warehouse_id"), primary_key=True)
    drugs_id = Column(Integer, ForeignKey("Drugs.id"), primary_key=True)
    quantity = Column(Integer)
    pharmacy_warehouse = relationship("PharmacyWarehouse", back_populates="drugs_association")
    drug = relationship("Drugs", back_populates="warehouse_association")
    __table_args__ = (PrimaryKeyConstraint('pharmacy_warehouse_id', 'drugs_id', name='pk_pharmacy_warehouse_drugs_join'),)

class PatientFollowingDrugs(Base):
    __tablename__ = "Patient_following_drugs"
    user_id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    drug_id = Column(Integer, ForeignKey("Drugs.id"), primary_key=True)
    user = relationship("User", back_populates="followed_drugs_association")
    drug = relationship("Drugs", back_populates="followed_by_users_association")
    __table_args__ = (PrimaryKeyConstraint('user_id', 'drug_id', name='pk_patient_following_drugs'),)
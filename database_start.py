from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import bcrypt
from dotenv import load_dotenv
import os
import psycopg2
from datetime import datetime

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    type = Column(String(50), nullable=False)  
    

    pharmacies_warehouses = relationship("PharmacyWarehouse", back_populates="user")
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', type='{self.type}')>"
    
    def set_password(self, password):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def check_password(self, password):
        password_bytes = password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, self.password_hash.encode('utf-8'))


class Drugs(Base):
    __tablename__ = 'drugs'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    batch_number = Column(String(100))
    active_substance = Column(String(200))
    remove_status = Column(String(50), nullable=False, default="active") 
    description = Column(String(500))
    date = Column(Date)
    
    pharmacy_warehouses = relationship("PharmacyWarehouseDrugsJoin", back_populates="drug")
    
    def __repr__(self):
        return f"<Drug(name='{self.name}', active_substance='{self.active_substance}')>"


class PharmacyWarehouse(Base):
    __tablename__ = 'pharmacy_warehouse'
    
    pharmacy_warehouse_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(200), nullable=False)
    localization = Column(String(200))
    
    user = relationship("User", back_populates="pharmacies_warehouses")
    drugs = relationship("PharmacyWarehouseDrugsJoin", back_populates="pharmacy_warehouse")
    
    def __repr__(self):
        return f"<PharmacyWarehouse(name='{self.name}', localization='{self.localization}')>"


class PharmacyWarehouseDrugsJoin(Base):
    __tablename__ = 'pharmacy_warehouse_drugs_join'
    
    pharmacy_warehouse_id = Column(Integer, ForeignKey('pharmacy_warehouse.pharmacy_warehouse_id'), primary_key=True)
    drugs_id = Column(Integer, ForeignKey('drugs.id'), primary_key=True)
    quantity = Column(Integer, default=0)
    

    pharmacy_warehouse = relationship("PharmacyWarehouse", back_populates="drugs")
    drug = relationship("Drugs", back_populates="pharmacy_warehouses")
    
    def __repr__(self):
        return f"<PharmacyWarehouseDrugsJoin(warehouse_id={self.pharmacy_warehouse_id}, drug_id={self.drugs_id}, quantity={self.quantity})>"


Base.metadata.create_all(engine)
print("Database tables created successfully.")
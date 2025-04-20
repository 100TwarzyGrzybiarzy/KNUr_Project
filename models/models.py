from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
import enum


class RemoveStatusEnum(str, enum.Enum):
     wycofany = "wycofany"
     wstrzymana_dystrybucja = "wstrzymana_dystrybucja"
     aktywny = "aktywny"


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserBase(BaseModel):
    username: str
    email: EmailStr
    type: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    type: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str


class DrugBase(BaseModel):
    name: str
    batch_number: Optional[str] = None
    active_substance: Optional[str] = None
    remove_status: RemoveStatusEnum
    description: Optional[str] = None
    date: Optional[date] = None

class DrugCreate(DrugBase):
    pass

class DrugUpdate(BaseModel):
    name: Optional[str] = None
    batch_number: Optional[str] = None
    active_substance: Optional[str] = None
    remove_status: Optional[RemoveStatusEnum] = None
    description: Optional[str] = None
    date: Optional[date] = None

class Drug(DrugBase):
    id: int

    class Config:
        from_attributes = True

class PharmacyWarehouseBase(BaseModel):
    name: str
    localization: Optional[str] = None

class PharmacyWarehouseCreate(PharmacyWarehouseBase):
    user_id: int

class PharmacyWarehouseUpdate(BaseModel):
    name: Optional[str] = None
    localization: Optional[str] = None

class PharmacyWarehouse(PharmacyWarehouseBase):
    pharmacy_warehouse_id: int
    user_id: int
    class Config:
        from_attributes = True

class PharmacyWarehouseDrugLink(BaseModel):
    pharmacy_warehouse_id: int
    drugs_id: int
    quantity: Optional[int] = None

    class Config:
        from_attributes = True

class PatientFollowRequest(BaseModel):
    drug_id: int

class PatientFollowingResponse(BaseModel):
    user_id: int
    drug_id: int

    class Config:
        from_attributes = True
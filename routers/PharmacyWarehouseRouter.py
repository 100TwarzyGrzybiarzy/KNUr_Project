from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List

from models.models import PharmacyWarehouse, PharmacyWarehouseCreate, PharmacyWarehouseUpdate, PharmacyWarehouseDrugLink
from schema.schema import User as UserModel
from services.PharmacyWarehouseService import pharmacyWarehouseService
from services.AuthService import get_current_user
from database import get_db

router = APIRouter(
    prefix="/warehouses",
    tags=["Pharmacy Warehouses"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=PharmacyWarehouse, status_code=status.HTTP_201_CREATED)
def create_warehouse_route(warehouse: PharmacyWarehouseCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return pharmacyWarehouseService.create_new_warehouse(db=db, warehouse=warehouse, current_user=current_user)

@router.get("/{warehouse_id}", response_model=PharmacyWarehouse)
def read_warehouse_route(warehouse_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_warehouse = pharmacyWarehouseService.read_warehouse(db=db, warehouse_id=warehouse_id, current_user=current_user)
    return db_warehouse

@router.get("/", response_model=List[PharmacyWarehouse])
def read_warehouses_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    warehouses = pharmacyWarehouseService.read_warehouses(db=db, skip=skip, limit=limit)
    return warehouses

@router.get("/user/{user_id}", response_model=List[PharmacyWarehouse])
def read_user_warehouses_route(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return pharmacyWarehouseService.read_user_warehouses(db=db, user_id=user_id, current_user=current_user, skip=skip, limit=limit)


@router.put("/{warehouse_id}", response_model=PharmacyWarehouse)
def update_warehouse_route(warehouse_id: int, warehouse: PharmacyWarehouseUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return pharmacyWarehouseService.update_existing_warehouse(db=db, warehouse_id=warehouse_id, warehouse_update=warehouse, current_user=current_user)

@router.delete("/{warehouse_id}", response_model=PharmacyWarehouse)
def delete_warehouse_route(warehouse_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return pharmacyWarehouseService.delete_existing_warehouse(db=db, warehouse_id=warehouse_id, current_user=current_user)


@router.post("/link_drug", response_model=PharmacyWarehouseDrugLink, status_code=status.HTTP_201_CREATED)
def link_drug_to_warehouse_route(link_data: PharmacyWarehouseDrugLink, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    # Service returns the SQLAlchemy JoinModel, FastAPI converts using from_attributes=True in Pydantic model
    link_db = pharmacyWarehouseService.link_drug_to_warehouse(db=db, link_data=link_data, current_user=current_user)
    return link_db

@router.delete("/{warehouse_id}/drugs/{drug_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_drug_from_warehouse_route(warehouse_id: int, drug_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    pharmacyWarehouseService.unlink_drug_from_warehouse(db=db, warehouse_id=warehouse_id, drug_id=drug_id, current_user=current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
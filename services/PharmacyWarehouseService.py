from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from repositories.PharmacyWarehouseRepository import pharmacyWarehouseRepository
from repositories.PharmacyWarehouseDrugsJoinRepository import pharmacyWarehouseDrugsJoinRepository
from repositories.UserRepository import userRepository
from repositories.DrugRepository import drugRepository
from models.models import PharmacyWarehouseCreate, PharmacyWarehouseUpdate, PharmacyWarehouse, PharmacyWarehouseDrugLink
from schema.schema import PharmacyWarehouse as WarehouseModel
from schema.schema import User as UserModel
from schema.schema import PharmacyWarehouseDrugsJoin as JoinModel

class PharmacyWarehouseService:

    def create_new_warehouse(self, db: Session, warehouse: PharmacyWarehouseCreate, current_user: UserModel) -> WarehouseModel:
        if warehouse.user_id != current_user.id and current_user.type != "admin":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot create warehouse for another user")

        owner = userRepository.get_user(db, warehouse.user_id)
        if not owner:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {warehouse.user_id} not found")

        return pharmacyWarehouseRepository.create_warehouse(db=db, warehouse=warehouse)

    def read_warehouse(self, db: Session, warehouse_id: int, current_user: Optional[UserModel] = None) -> Optional[WarehouseModel]:
        db_warehouse = pharmacyWarehouseRepository.get_warehouse(db, warehouse_id=warehouse_id)
        if db_warehouse is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
        return db_warehouse

    def read_warehouses(self, db: Session, skip: int = 0, limit: int = 100) -> List[WarehouseModel]:
        return pharmacyWarehouseRepository.get_warehouses(db, skip=skip, limit=limit)

    def read_user_warehouses(self, db: Session, user_id: int, current_user: UserModel, skip: int = 0, limit: int = 100) -> List[WarehouseModel]:
        if user_id != current_user.id and current_user.type != "admin":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view these warehouses")
        user = userRepository.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
        return pharmacyWarehouseRepository.get_warehouses_by_user(db, user_id=user_id, skip=skip, limit=limit)


    def update_existing_warehouse(self, db: Session, warehouse_id: int, warehouse_update: PharmacyWarehouseUpdate, current_user: UserModel) -> Optional[WarehouseModel]:
        db_warehouse = self.read_warehouse(db, warehouse_id, current_user) # Use internal read which checks existence
        if db_warehouse.user_id != current_user.id and current_user.type != "admin":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this warehouse")

        updated_warehouse = pharmacyWarehouseRepository.update_warehouse(db=db, warehouse_id=warehouse_id, warehouse_update=warehouse_update)
        return updated_warehouse

    def delete_existing_warehouse(self, db: Session, warehouse_id: int, current_user: UserModel) -> Optional[WarehouseModel]:
        db_warehouse = self.read_warehouse(db, warehouse_id, current_user) # Use internal read which checks existence
        if db_warehouse.user_id != current_user.id and current_user.type != "admin":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this warehouse")

        db.query(JoinModel).filter(JoinModel.pharmacy_warehouse_id == warehouse_id).delete(synchronize_session=False)
        db.commit()

        deleted_warehouse = pharmacyWarehouseRepository.delete_warehouse(db=db, warehouse_id=warehouse_id)
        return deleted_warehouse

    def link_drug_to_warehouse(self, db: Session, link_data: PharmacyWarehouseDrugLink, current_user: UserModel) -> JoinModel:
        warehouse = self.read_warehouse(db, link_data.pharmacy_warehouse_id, current_user) # Checks existence
        if warehouse.user_id != current_user.id and current_user.type != "admin":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this warehouse")

        drug = drugRepository.get_drug(db, link_data.drugs_id)
        if not drug:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drug not found")

        link = pharmacyWarehouseDrugsJoinRepository.add_or_update_drug_in_warehouse(db, link_data)
        return link


    def unlink_drug_from_warehouse(self, db: Session, warehouse_id: int, drug_id: int, current_user: UserModel) -> None:
        warehouse = self.read_warehouse(db, warehouse_id, current_user) # Checks existence
        if warehouse.user_id != current_user.id and current_user.type != "admin":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to modify this warehouse")

        removed = pharmacyWarehouseDrugsJoinRepository.remove_drug_from_warehouse(db, warehouse_id, drug_id)
        if not removed:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drug link not found in this warehouse")
        return


pharmacyWarehouseService = PharmacyWarehouseService()
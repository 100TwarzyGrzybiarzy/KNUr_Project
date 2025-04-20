from sqlalchemy.orm import Session
from typing import Optional, List
from schema.schema import PharmacyWarehouse
from models.models import PharmacyWarehouseCreate, PharmacyWarehouseUpdate

class PharmacyWarehouseRepository:

    def get_warehouse(self, db: Session, warehouse_id: int) -> Optional[PharmacyWarehouse]:
        return db.query(PharmacyWarehouse).filter(PharmacyWarehouse.pharmacy_warehouse_id == warehouse_id).first()

    def get_warehouses(self, db: Session, skip: int = 0, limit: int = 100) -> List[PharmacyWarehouse]:
        return db.query(PharmacyWarehouse).offset(skip).limit(limit).all()

    def get_warehouses_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[PharmacyWarehouse]:
        return db.query(PharmacyWarehouse).filter(PharmacyWarehouse.user_id == user_id).offset(skip).limit(limit).all()

    def create_warehouse(self, db: Session, warehouse: PharmacyWarehouseCreate) -> PharmacyWarehouse:
        db_warehouse = PharmacyWarehouse(**warehouse.model_dump())
        db.add(db_warehouse)
        db.commit()
        db.refresh(db_warehouse)
        return db_warehouse

    def update_warehouse(self, db: Session, warehouse_id: int, warehouse_update: PharmacyWarehouseUpdate) -> Optional[PharmacyWarehouse]:
        db_warehouse = self.get_warehouse(db, warehouse_id)
        if not db_warehouse:
            return None

        update_data = warehouse_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_warehouse, key, value)

        db.add(db_warehouse)
        db.commit()
        db.refresh(db_warehouse)
        return db_warehouse

    def delete_warehouse(self, db: Session, warehouse_id: int) -> Optional[PharmacyWarehouse]:
        db_warehouse = self.get_warehouse(db, warehouse_id)
        if db_warehouse:
            db.delete(db_warehouse)
            db.commit()
            return db_warehouse
        return None

pharmacyWarehouseRepository = PharmacyWarehouseRepository()
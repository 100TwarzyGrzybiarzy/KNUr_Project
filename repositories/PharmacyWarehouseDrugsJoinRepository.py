from sqlalchemy.orm import Session
from typing import Optional
from schema.schema import PharmacyWarehouseDrugsJoin
from models.models import PharmacyWarehouseDrugLink

class PharmacyWarehouseDrugsJoinRepository:

    def get_link(self, db: Session, warehouse_id: int, drug_id: int) -> Optional[PharmacyWarehouseDrugsJoin]:
        return db.query(PharmacyWarehouseDrugsJoin).filter(
            PharmacyWarehouseDrugsJoin.pharmacy_warehouse_id == warehouse_id,
            PharmacyWarehouseDrugsJoin.drugs_id == drug_id
        ).first()

    def add_or_update_drug_in_warehouse(self, db: Session, link_data: PharmacyWarehouseDrugLink) -> PharmacyWarehouseDrugsJoin:
        db_link = self.get_link(db, link_data.pharmacy_warehouse_id, link_data.drugs_id)
        if db_link:
            if link_data.quantity is not None:
                db_link.quantity = link_data.quantity
        else:
            db_link = PharmacyWarehouseDrugsJoin(**link_data.model_dump())
            db.add(db_link)
        db.commit()
        db.refresh(db_link)
        return db_link

    def remove_drug_from_warehouse(self, db: Session, warehouse_id: int, drug_id: int) -> bool:
        db_link = self.get_link(db, warehouse_id, drug_id)
        if db_link:
            db.delete(db_link)
            db.commit()
            return True
        return False

pharmacyWarehouseDrugsJoinRepository = PharmacyWarehouseDrugsJoinRepository()
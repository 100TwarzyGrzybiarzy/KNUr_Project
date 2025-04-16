from database_start import Base, User, Drugs, PharmacyWarehouse, PharmacyWarehouseDrugsJoin

"""USERS"""

def get_all_users(session):
    return session.query(User).all()

def get_user_by_id(session, user_id):
    return session.query(User).filter_by(id=user_id).first()

"""PHARMACIES/WAREHOUSES"""

def get_all_pharmacies(session):
    return session.query(PharmacyWarehouse).all()

def get_pharmacy_by_id(session, pharmacy_id):
    return session.query(PharmacyWarehouse).filter_by(pharmacy_warehouse_id=pharmacy_id).first()

"""DRUGS"""

def get_drug_by_id(session, drug_id):
    return session.query(Drugs).filter_by(id=drug_id).first()

def get_drug_by_name(session, drug_name):
    return session.query(Drugs).filter_by(name=drug_name).first()

def get_all_drugs(session):
    return session.query(Drugs).all()

def get_drug_quantity_in_pharmacy(session, pharmacy_id, drug_id):
    return session.query(PharmacyWarehouseDrugsJoin).filter_by(pharmacy_warehouse_id=pharmacy_id, drugs_id=drug_id).first()

def get_drug_quantity_in_all_pharmacies(session, drug_id):
    return session.query(PharmacyWarehouseDrugsJoin).filter_by(drugs_id=drug_id).all()
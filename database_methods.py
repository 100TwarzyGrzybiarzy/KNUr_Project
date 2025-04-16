from database_start import Base, User, Drugs, PharmacyWarehouse, PharmacyWarehouseDrugsJoin
from datetime import datetime
import bcrypt

def add_user(session, username, email, password, type):
    hashed_password = set_password(password)
    new_user = User(username=username, password_hash=hashed_password, email=email, type=type)
    session.add(new_user)
    session.commit()
    return new_user

def delete_user(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return True
    return False

def update_user(session, user_id, username=None, password=None):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        if username:
            user.username = username
        if password:
            user.set_password(password)
        session.commit()
        return True
    return False

def add_drug(session, name, batch_number=None, active_substance=None, description=None, date=datetime.now().date(), remove_status="active"):
    new_drug = Drugs(name=name, batch_number=batch_number, active_substance=active_substance,
                     description=description, date=date, remove_status=remove_status)
    session.add(new_drug)
    session.commit()
    return new_drug

def add_pharmacy(session, user_id, name, localization=None):
    new_pharmacy = PharmacyWarehouse(
        user_id=user_id,
        name=name,
        localization=localization
    )
    session.add(new_pharmacy)
    session.commit()
    return new_pharmacy

def add_drug_to_pharmacy(session, pharmacy_id, drug_id, quantity):
    drug_in_pharmacy = PharmacyWarehouseDrugsJoin(
        pharmacy_warehouse_id=pharmacy_id,
        drugs_id=drug_id,
        quantity=quantity
    )
    session.add(drug_in_pharmacy)
    session.commit()
    return drug_in_pharmacy

def set_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    return password_hash

def check_password(user, password):
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, user.password_hash.encode('utf-8'))
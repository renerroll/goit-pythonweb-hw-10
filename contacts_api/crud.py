from sqlalchemy.orm import Session
from contacts_api.models import Contact, User
from datetime import date, timedelta

def get_contacts(db: Session, user_id: int):
    return db.query(Contact).filter(Contact.user_id == user_id).all()

def get_contact_by_id(db: Session, user_id: int, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user_id).first()

def create_contact(db: Session, user_id: int, contact_data: dict):
    contact = Contact(**contact_data, user_id=user_id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

def update_contact(db: Session, user_id: int, contact_id: int, update_data: dict):
    contact = get_contact_by_id(db, user_id, contact_id)
    if contact is None:
            return None
    for key, value in update_data.items():
        setattr(contact, key, value)
    db.commit()
    return contact

def delete_contact(db: Session, user_id: int, contact_id: int):
    contact = get_contact_by_id(db, user_id, contact_id)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
    
def search_contacts(db: Session, user_id: int, query: str):
    return db.query(Contact).filter(
        Contact.user_id == user_id,
        (
            (Contact.first_name.ilike(f"%{query}%")) |
            (Contact.last_name.ilike(f"%{query}%")) |
            (Contact.email.ilike(f"%{query}%"))
        )
    ).all()

def get_upcoming_birthdays(db: Session, user_id: int):
    today = date.today()
    upcoming = today + timedelta(days=7)
    return db.query(Contact).filter(
        Contact.user_id == user_id,
        Contact.birthday.between(today, upcoming)
    ).all()

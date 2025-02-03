from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from contacts_api.configs.database import engine, SessionLocal
from contacts_api import crud, models, schemas
from contacts_api.auth import decode_access_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["http://localhost:*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = crud.get_user_by_id(db, user_id=payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user

@app.get("/")
async def read_root():
    return {"message": "Welcome to the database"}

@app.post("/contacts/", response_model=schemas.ContactOut)
def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.create_contact(db, contact, user_id=user.id)

@app.get("/contacts/", response_model=list[schemas.ContactOut])
def read_contacts(
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.get_contacts(db, user_id=user.id)

@app.get("/contacts/{contact_id}", response_model=schemas.ContactOut)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    contact = crud.get_contact_by_id(db, contact_id)
    if not contact or contact.user_id != user.id:
        raise HTTPException(status_code=404, detail="Contact not found or access denied")
    return contact

@app.put("/contacts/{contact_id}", response_model=schemas.ContactOut)
def update_contact(
    contact_id: int,
    contact: schemas.ContactUpdate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    update_contact = crud.update_contact(db, contact_id, contact, user_id=user.id)
    if not update_contact:
        raise HTTPException(status_code=404, detail="Contact not found or access denied")
    return update_contact

@app.delete("/contacts/{contact_id}", response_model=schemas.ContactOut)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    delete_contact = crud.delete_contact(db, contact_id, user_id=user.id)
    if not delete_contact:
        raise HTTPException(status_code=404, detail="Contact not found or access denied")
    return delete_contact

@app.get("/contacts/search/")
def search_contacts(
    query: str,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.search_contacts(db, query, user_id=user.id)

@app.get("/contacts/birthdays/", response_model=list[schemas.ContactOut])
def upcoming_birthdays(
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_current_user),
):
    return crud.get_upcoming_birthdays(db, user_id=user.id)
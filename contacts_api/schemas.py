from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import date

class User(BaseModel):
   id: int
   username: str
   email: EmailStr = Field(max_length=50)
   avatar: str

   model_config = ConfigDict(from_attributes=True)

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str]

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    birthday: Optional[date]
    additional_info: Optional[str]

class ContactOut(ContactBase):
    id: int

    class Config:
        orm_mode = True

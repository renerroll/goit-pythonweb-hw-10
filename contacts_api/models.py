from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from .configs.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)  # Додано
    avatar_url = Column(String, nullable=True)

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    phone_number = Column(String)
    birthday = Column(Date)
    extra_data = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="contacts")

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.db import Base


class User(Base):
    __tablename__ = "user"
    uid = Column(String, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    dialogs = relationship("UserDialog", back_populates="user")


class Token(Base):
    __tablename__ = "token"
    uid = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.uid"))
    access_token = Column(String)
    refresh_token = Column(String)
    expires_date = Column(DateTime)
    token_type = Column(String)

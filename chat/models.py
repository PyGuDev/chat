from re import S
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base


class BaseModel:
    uid = Column(String, primary_key=True, index=True)


class Dialog(BaseModel, Base):
    __tablename__ = "dialog"
    name = Column(String)
    messages = relationship("Message", back_populates="dialog")
    users = relationship("UserDialog", back_populates="dialog")


class UserDialog(BaseModel, Base):
    __tablename__ = "user_dialog"
    user_id = Column(String, ForeignKey("user.uid"))
    user = relationship("User", back_populates="dialogs")
    dialog_id = Column(String, ForeignKey("dialog.uid"))
    dialog = relationship("Dialog", back_populates="users")


class Message(BaseModel, Base):
    __tablename__ = "message"
    text = Column(String)
    created_at = Column(DateTime)
    readed = Column(Boolean)
    dialog_id = Column(String, ForeignKey("dialog.uid"))
    dialog = relationship("Dialog", back_populates="messages")
    author_id = Column(String, ForeignKey("user.uid"))
    author = relationship("User")


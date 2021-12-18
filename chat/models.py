from re import S
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base


class User(Base):
    __tablename__ = "user"
    uid = Column(String, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    dialogs = relationship("UserDialog", back_populates="user")


class Dialog(Base):
    __tablename__ = "dialog"
    uid = Column(String, primary_key=True, index=True)
    name = Column(String)
    messages = relationship("Message", back_populates="dialog")
    users = relationship("UserDialog", back_populates="dialog")


class UserDialog(Base):
    __tablename__ = "user_dialog"
    uid = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.uid"))
    user = relationship("User", back_populates="dialogs")
    dialog_id = Column(String, ForeignKey("dialog.uid"))
    dialog = relationship("Dialog", back_populates="users")


class Message(Base):
    __tablename__ = "message"
    uid = Column(String, primary_key=True, index=True)
    text = Column(String)
    created_at = Column(DateTime)
    readed = Column(Boolean)
    dialog_id = Column(String, ForeignKey("dialog.uid"))
    dialog = relationship("Dialog", back_populates="messages")
    author_id = Column(String, ForeignKey("user.uid"))
    author = relationship("User")


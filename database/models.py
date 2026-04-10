from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List
from database.session import Base


class Room(Base):
    __tablename__="rooms"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_name: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    users: Mapped[List["User"]] = relationship("User", back_populates="room")
    
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    
    room: Mapped["Room"] = relationship("Room", back_populates="users")

class Message(Base):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    type: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    